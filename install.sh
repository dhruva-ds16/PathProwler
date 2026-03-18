#!/bin/bash
# PathProwler - Installation Script for Linux/Mac
# Prowl through paths and discover hidden treasures 🐾
# This script creates a virtual environment, installs dependencies, and runs the TUI

echo "========================================"
echo "  PathProwler - Installation Script  "
echo "========================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Check if Python is installed
echo -e "${YELLOW}[*] Checking Python installation...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}[+] Found: $PYTHON_VERSION${NC}"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version)
    echo -e "${GREEN}[+] Found: $PYTHON_VERSION${NC}"
    PYTHON_CMD="python"
else
    echo -e "${RED}[!] ERROR: Python is not installed${NC}"
    echo -e "${RED}[!] Please install Python 3.8+ from your package manager${NC}"
    exit 1
fi

# Check if gobuster is installed
echo -e "${YELLOW}[*] Checking gobuster installation...${NC}"
if command -v gobuster &> /dev/null; then
    echo -e "${GREEN}[+] Found: gobuster${NC}"
else
    echo -e "${YELLOW}[!] WARNING: gobuster is not installed or not in PATH${NC}"
    echo -e "${YELLOW}[!] Please install gobuster:${NC}"
    echo -e "${YELLOW}    - Ubuntu/Debian: sudo apt install gobuster${NC}"
    echo -e "${YELLOW}    - Arch: sudo pacman -S gobuster${NC}"
    echo -e "${YELLOW}    - macOS: brew install gobuster${NC}"
    echo -e "${YELLOW}    - Or from: https://github.com/OJ/gobuster${NC}"
    echo -e "${YELLOW}[!] The tool will not work without gobuster!${NC}"
    echo ""
fi

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}[!] ERROR: requirements.txt not found${NC}"
    echo -e "${RED}[!] Please ensure you're running this script from the Automation directory${NC}"
    exit 1
fi

# Create virtual environment
echo ""
echo -e "${YELLOW}[*] Creating virtual environment...${NC}"
if [ -d "venv" ]; then
    echo -e "${CYAN}[*] Virtual environment already exists, skipping creation...${NC}"
else
    $PYTHON_CMD -m venv venv
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}[+] Virtual environment created successfully${NC}"
    else
        echo -e "${RED}[!] ERROR: Failed to create virtual environment${NC}"
        exit 1
    fi
fi

# Activate virtual environment and install dependencies
echo ""
echo -e "${YELLOW}[*] Installing dependencies...${NC}"
source venv/bin/activate
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[+] Dependencies installed successfully${NC}"
else
    echo -e "${RED}[!] ERROR: Failed to install dependencies${NC}"
    exit 1
fi

# Installation complete
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Installation Complete!              ${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${CYAN}To run PathProwler TUI:${NC}"
echo -e "  ${NC}./run.sh${NC}"
echo ""
echo -e "${CYAN}To run CLI version:${NC}"
echo -e "  ${NC}./venv/bin/python pathprowler.py -u http://target.com -m all${NC}"
echo ""
echo -e "${CYAN}To activate the virtual environment manually:${NC}"
echo -e "  ${NC}source venv/bin/activate${NC}"
echo ""

# Ask if user wants to run the TUI now
echo -e "${YELLOW}Would you like to run the TUI now? (y/n): ${NC}"
read -r response

if [[ "$response" =~ ^[Yy]$ ]]; then
    echo ""
    echo -e "${CYAN}[*] Starting PathProwler TUI...${NC}"
    echo ""
    ./venv/bin/python pathprowler_tui.py
else
    echo ""
    echo -e "${CYAN}[*] You can run the TUI anytime with: ./run.sh${NC}"
fi
