import argparse
import logging
import os
import sys
import pdfplumber
import pandas as pd
from google import genai
from dotenv import load_dotenv

# Modular imports
from src.logic.processor import normalize_df, parse_md, extract_from_page
from src.config import DEFAULT_PROMPT

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def main(pdf_files, output_path, save_md=False, save_csv=False, clean=False):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    load_dotenv(os.path.join(base_dir, "api_key.env"))
    api_key = os.getenv("API_KEY")
    
    if not api_key:
        logger.error("API_KEY not found in api_key.env")
        sys.exit(1)

    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        logger.error(f"Failed to initialize Gemini client: {e}")
        sys.exit(1)

    out_dir = os.path.dirname(output_path) or "."
    os.makedirs(out_dir, exist_ok=True)

    writer = pd.ExcelWriter(output_path, engine='openpyxl')
    
    for pdf_path in pdf_files:
        logger.info(f"Processing: {os.path.basename(pdf_path)}")
        all_results = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    res = extract_from_page(client, page, DEFAULT_PROMPT, 
                                          lambda p: logger.info(f"  - Analyzing page {p}..."))
                    all_results.extend(res)
            
            if all_results:
                processed = []
                for res in all_results:
                    df = res['df']
                    if clean: df = normalize_df(df)
                    processed.append({"df": df, "md": res['md']})
                
                combined_df = pd.concat([p['df'] for p in processed], ignore_index=True)
                short_name = os.path.splitext(os.path.basename(pdf_path))[0]
                combined_df.to_excel(writer, sheet_name=short_name[:31], index=False, header=False)
                
                if save_md:
                    md_path = f"{os.path.splitext(pdf_path)[0]}.md"
                    with open(md_path, 'w', encoding='utf-8') as f:
                        for p in processed: f.write(p['md'] + "\n\n")
                    logger.info(f"  + Saved MD: {os.path.basename(md_path)}")
                
                if save_csv:
                    csv_path = f"{os.path.splitext(pdf_path)[0]}.csv"
                    combined_df.to_csv(csv_path, index=False, header=False)
                    logger.info(f"  + Saved CSV: {os.path.basename(csv_path)}")
        except Exception as e:
            logger.error(f"Error processing {pdf_path}: {e}")

    writer.close()
    logger.info(f"Done. Results saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract tables from PDF using Gemini AI.")
    parser.add_argument("pdf_files", nargs="+", help="PDF files to process")
    parser.add_argument("--output", "-o", default="output.xlsx", help="Output Excel file")
    parser.add_argument("--md", action="store_true", help="Save as Markdown")
    parser.add_argument("--csv", action="store_true", help="Save as CSV")
    parser.add_argument("--clean", action="store_true", help="Clean/normalize data")
    
    args = parser.parse_args()
    main(args.pdf_files, args.output, args.md, args.csv, args.clean)
