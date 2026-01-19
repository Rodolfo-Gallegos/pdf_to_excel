# PDF to EXCEL/CSV/MD AI extractor

An AI-powered tool that extracts tables from PDF files by analyzing pages as images using the Gemini 3 Flash Preview model. Captures complex visual layouts that traditional text-based extractors fail to process.

## 📊 Result showcase

### Input vs. Output

| 1. Source PDF | 2. Excel Result | 3. Markdown Result | 4. CSV Result |
| :---: | :---: | :---: | :---: |
| ![Original PDF](screenshots/pdf_tables.png) | ![Excel Output](screenshots/xlsx_table.png) | ![Markdown Output](screenshots/markdown_table.png) | ![CSV Output](screenshots/csv_table.png) |

> [!TIP]
> **From pdf image to structured data in seconds.** Perfect for scanned documents and complex reports.

## ✨ Features

- **Multimodal AI**: Uses computer vision to extract tables exactly as they appear.
- **Graphical Interface (GUI)**: User-friendly interface with real-time logs and progress tracking.
- **Multi-format Export**: Save results to **Excel (.xlsx)**, **CSV**, and **Markdown**.
- **Data Cleaning**: Optional normalization to remove currency symbols and fix numeric formats.
- **Automated Setup**: One-click installers for **Windows (.bat)** and **Linux/macOS (.sh)**.
- **Selective Processing**: Ask for specific pages (e.g., "Page 2").

## 📂 Project Structure

```text
PDF_to_XLSX/
├── EJECUTAR_WINDOWS.bat  # Main Windows launcher
├── EJECUTAR_LINUX.sh    # Main Linux/macOS launcher
├── README.md            # Quick start guide
├── docs/                # Manuals and screenshots
│   ├── Manual_ES.md
│   └── Manual_EN.md
└── src/                 # Source code and assets
    ├── assets/icons/    # Icon assets
    ├── ui/              # User Interface
    ├── logic/           # Processing logic
    ├── main.py          # GUI Entry point
    ├── cli.py           # CLI Entry point
    └── api_key.env      # API Key configuration
```

## 🚀 Quick Start

### For Windows

1. Double-click **`EJECUTAR_WINDOWS.bat`**.
2. It will automatically install Python (if missing), setup dependencies, and create a desktop shortcut.

### For Linux & macOS

1. Open a terminal in the folder.
2. Run: `chmod +x EJECUTAR_LINUX.sh`
3. Run: `./EJECUTAR_LINUX.sh`

---

## 🛠 How to Use

### Version 1: Graphical interface (GUI)

Launch the app to manage everything visually:

```bash
python src/main.py
```

### Version 2: Command Line (CLI)

Run the script directly for quick processing:

```bash
python src/cli.py file1.pdf file2.pdf --output results.xlsx
```

---

## ⚙️ Configuration & API Key

### 1. Requirements

- Python 3.8+
- A Google Gemini API Key

### 2. Setup your API Key

1. Get your free API key from [Google AI Studio](https://aistudio.google.com/api-keys).
2. Edit the `src/api_key.env` file and replace the placeholder:

   ```env
   API_KEY=your_gemini_api_key_here
   ```

## 🏗 Technical details

1. **Rendering**: Uses `pdfplumber` to convert pages to 300 DPI images.
2. **Analysis**: Images are sent to **Gemini 3 Flash Preview** for table detection.
3. **Parsing**: AI Markdown is converted into `pandas` DataFrames.
4. **Writing**: Results are consolidated using `openpyxl`.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
