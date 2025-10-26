#!/bin/bash
#
# Grape Backend - Installation Script
# Usage: ./install.sh
#

set -e

echo "Grape Backend - Installation"
echo "================================"
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "[!] uv is not installed"
    echo "[*] Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo "[+] uv installed"
    echo "[!] Please restart your terminal and run this script again"
    exit 0
fi

echo "[+] uv detected: $(uv --version)"
echo ""

# Create virtual environment
echo "[*] Creating Python 3.12 virtual environment..."
uv venv --python 3.12

# Detect OS for activation command
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    ACTIVATE_CMD=".venv\\Scripts\\activate"
else
    ACTIVATE_CMD="source .venv/bin/activate"
fi

echo "[+] Virtual environment created"
echo ""

# Activate venv and install dependencies
echo "[*] Installing Python dependencies..."
uv pip install -r requirements.txt

# Install pip in venv (required for spacy download)
echo "[*] Installing pip in venv..."
uv pip install pip

echo "[+] Dependencies installed"
echo ""

# Install Spacy models
echo "[*] Downloading Spacy models..."
.venv/bin/python -m spacy download en_core_web_sm
.venv/bin/python -m spacy download en_core_web_lg

echo "[+] Spacy models installed"
echo ""

# Optional: Install scispacy models
read -p "Do you want to install scientific models (scispacy)? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "[*] Installing scispacy models..."
    uv pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/en_core_sci_lg-0.5.4.tar.gz
    uv pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/en_ner_bionlp13cg_md-0.5.4.tar.gz
    uv pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/en_ner_craft_md-0.5.4.tar.gz
    echo "[+] Scispacy models installed"
fi

echo ""

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "[*] Creating .env file..."
    cp .env.example .env
    echo "[+] .env file created"
    echo "[!] Don't forget to configure your API keys in .env"
else
    echo "[i] .env file already exists"
fi

echo ""
echo "[+] Installation complete!"
echo ""
echo "To start the server:"
echo "   1. Activate venv: $ACTIVATE_CMD"
echo "   2. Configure .env with your API keys"
echo "   3. Run: python main.py (recommended)"
echo "   4. Or: uvicorn main:app --reload"
echo ""
echo "Documentation: http://localhost:8000/docs"
echo "Health check: http://localhost:8000/api/health"
echo ""
