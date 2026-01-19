# Extractor de PDF a EXCEL/CSV/MD con IA

Una herramienta potenciada por IA que extrae tablas de archivos PDF analizando las páginas como imágenes mediante el modelo Gemini 3 Flash Preview.

## 📊 Resumen de resultados

### PDF Origen vs. Salida

| 1. PDF Original | 2. Resultado Excel | 3. Resultado Markdown | 4. Resultado CSV |
| :---: | :---: | :---: | :---: |
| ![PDF Original](screenshots/pdf_tables.png) | ![Salida Excel](screenshots/xlsx_table.png) | ![Salida Markdown](screenshots/markdown_table.png) | ![Salida CSV](screenshots/csv_table.png) |

> [!TIP]
> **De imagen en pdf a datos estructurados en segundos.** Ideal para documentos escaneados y reportes complejos.

## ✨ Características

- **IA Multimodal**: Utiliza visión artificial para extraer tablas exactamente como aparecen.
- **Interfaz Gráfica (GUI)**: Pantalla de uso sencillo con registro en tiempo real.
- **Exportación Multi-formato**: guarda en **Excel (.xlsx)**, **CSV** y **Markdown**.
- **Limpieza de Datos**: Normalización opcional.
- **Instalación Automatizada**: Scripts de un solo clic.
- **Procesamiento Selectivo**: Indica páginas específicas (ej: "Página 2").

## 📂 Estructura del Proyecto

```text
PDF_to_XLSX/
├── EJECUTAR_WINDOWS.bat  # Lanzador principal Windows
├── EJECUTAR_LINUX.sh    # Lanzador principal Linux/macOS
├── README.md            # Guía rápida
├── docs/                # Manuales y capturas
│   ├── Manual_ES.md
│   └── Manual_EN.md
└── src/                 # Código fuente y activos
    ├── assets/icons/    # Iconos
    ├── ui/              # Interfaz
    ├── logic/           # Lógica de procesamiento
    ├── main.py          # Punto de entrada GUI
    ├── cli.py           # Punto de entrada CLI
    └── api_key.env      # Configuración de Clave API
```

## 🚀 Inicio Rápido

### En Windows

1. Haz doble clic en **`EJECUTAR_WINDOWS.bat`**.
2. Automáticamente instalará Python (si falta), las dependencias y creará un acceso directo en tu escritorio.

### En Linux & macOS

1. Abre una terminal en la carpeta.
2. Ejecuta: `chmod +x EJECUTAR_LINUX.sh`
3. Ejecuta: `./EJECUTAR_LINUX.sh`

---

## 🛠 Modo de uso

### Versión 1: Interfaz Gráfica (GUI)

```bash
python src/main.py
```

### Versión 2: Línea de Comandos (CLI)

```bash
python src/cli.py archivo1.pdf archivo2.pdf --output resultados.xlsx
```

## ⚙️ Configuración y llave API

1. Consigue tu clave gratuita en [Google AI Studio](https://aistudio.google.com/api-keys).
2. Edita el archivo `src/api_key.env` y sustituye el valor.

## 📜 Licencia

Este proyecto está bajo la Licencia MIT.
