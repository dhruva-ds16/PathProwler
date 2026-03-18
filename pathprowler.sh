#!/bin/bash
# PathProwler - Quick Launcher
# Prowl through paths and discover hidden treasures 🐾
# This script checks dependencies and launches the TUI

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Determine Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}✗ Python not found! Please install Python 3.8+${NC}"
    exit 1
fi

# Check if gobuster is installed
if ! command -v gobuster &> /dev/null; then
    echo -e "${YELLOW}⚠ Warning: gobuster not found!${NC}"
    echo -e "${YELLOW}  Install: sudo apt install gobuster (or brew install gobuster)${NC}"
    echo ""
fi

# Create venv if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${CYAN}Creating virtual environment...${NC}"
    $PYTHON_CMD -m venv venv
fi

# Activate venv and install/update dependencies quietly
source venv/bin/activate
pip install --upgrade pip -q > /dev/null 2>&1
pip install -r requirements.txt -q > /dev/null 2>&1

# Launch TUI
clear
echo -e "${CYAN}🐾 Launching PathProwler TUI...${NC}"
echo ""
./venv/bin/python pathprowler_tui.py
