import time
import re
import pandas as pd
from typing import List, Dict, Any, Optional
from google import genai
from PIL import Image

def normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans and normalizes DataFrame content."""
    def clean_cell(val):
        if pd.isna(val) or val is None: return ""
        s = str(val).strip()
        s = s.replace('$', '').replace('€', '').replace(',', '')
        try:
            if '.' in s: return float(s)
            return int(s)
        except ValueError:
            return s
    return df.apply(lambda col: col.map(clean_cell))

def parse_md(md_text: str) -> pd.DataFrame:
    """Parses Markdown table text into a pandas DataFrame."""
    lines = md_text.strip().split('\n')
    data = []
    for line in lines:
        if '|' in line:
            cells = [c.strip() for c in line.split('|')]
            if cells and cells[0] == '': cells = cells[1:]
            if cells and cells[-1] == '': cells = cells[:-1]
            if all(set(c) <= {'-', ':', ' '} for c in cells): continue
            if cells: data.append(cells)
        else:
            if line.strip(): data.append([line.strip()])
    
    if not data: return pd.DataFrame()
    
    max_cols = max(len(row) for row in data)
    norm_data = [row + [''] * (max_cols - len(row)) for row in data]
    return pd.DataFrame(norm_data)

def parse_page_query(prompt: str, total_pages: int) -> List[int]:
    """
    Parses the prompt to find page references like 'página 2', 'page 1-3', etc.
    Returns a list of 0-indexed page numbers.
    """
    prompt_lower = prompt.lower()
    
    # Check for keywords related to single pages or ranges
    # Examples: "página 2", "page 3", "páginas 1 a 3", "pages 2-4"
    patterns = [
        r"(?:p\u00e1gina|page)\s+(\d+)",           # "página 2"
        r"(?:p\u00e1ginas|pages)\s+(\d+)\s+(?:a|to|-)\s+(\d+)", # "páginas 1 a 3"
        r"(?:p\u00e1ginas|pages)\s+(\d+)(?:,)\s*(\d+)", # "páginas 1, 2" (simple case)
    ]
    
    selected_pages = set()
    
    # Pattern 1: Range "pages 1 to 3"
    range_match = re.search(r"(?:p\u00e1ginas|pages)\s+(\d+)\s*(?:a|to|-)\s*(\d+)", prompt_lower)
    if range_match:
        start = int(range_match.group(1))
        end = int(range_match.group(2))
        for p in range(start, end + 1):
            if 1 <= p <= total_pages:
                selected_pages.add(p - 1)
        return sorted(list(selected_pages))

    # Pattern 2: Single page "page 2"
    single_match = re.search(r"(?:p\u00e1gina|page)\s+(\d+)", prompt_lower)
    if single_match:
        p = int(single_match.group(1))
        if 1 <= p <= total_pages:
            selected_pages.add(p - 1)
        return sorted(list(selected_pages))

    # If no specific page found, return all pages
    return list(range(total_pages))

def extract_from_page(client: genai.Client, page: Any, prompt: str, log_callback=None, error_tracker: Dict[str, bool] = None) -> List[Dict[str, Any]]:
    """Extracts tables from a single PDF page."""
    if log_callback:
        log_callback(page.page_number)
        
    try:
        img = page.to_image(resolution=300).original
        
        max_retries = 1
        md_text = ""
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model='gemini-3-flash-preview',
                    contents=[prompt, img]
                )
                if response and hasattr(response, 'text') and response.text:
                    md_text = response.text
                break
            except Exception as e:
                if "400" in str(e):
                    if error_tracker is not None: error_tracker["has_error"] = True
                    raise e
                elif "429" in str(e):
                    if attempt < max_retries - 1:
                        time.sleep((attempt + 1) * 10)
                    else:
                        if error_tracker is not None: error_tracker["has_error"] = True
                        raise e
                else:
                    raise e
        
        clean_md = md_text.replace("```markdown", "").replace("```", "").strip()
        if clean_md:
            df = parse_md(clean_md)
            if not df.empty:
                return [{"df": df, "md": clean_md}]
    except Exception as e:
        if "400" in str(e) or "429" in str(e):
            raise e
        # Other errors are logged via callback or returned empty
    return []
