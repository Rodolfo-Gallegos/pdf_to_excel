#!/bin/bash

# ==================================================
#   PDF Table Extractor - Unix Launcher (Linux/macOS)
# ==================================================

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "--------------------------------------------------"
echo "   PDF Table Extractor - Launching..."
echo "--------------------------------------------------"

# Determinar comando de python
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo "Error: Python no está instalado / Python is not installed."
    exit 1
fi

# 2. Check if dependencies are installed
# We check for one of the main dependencies: google-genai
if ! $PYTHON_CMD -c "import google.genai" &> /dev/null
then
    echo "[*] Dependencies missing. Installing from requirements.txt..."
    $PYTHON_CMD -m pip install --upgrade pip
    $PYTHON_CMD -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[X] Failed to install dependencies. Check your internet connection or permissions."
        exit 1
    fi
    echo "[OK] Dependencies installed."
fi

# 3. Launch GUI
echo "[*] Starting Application..."
# Run in background and exit terminal
$PYTHON_CMD main.py &

echo "--------------------------------------------------"
echo "   Application started. You can close this window."
echo "--------------------------------------------------"
sleep 3
exit 0
