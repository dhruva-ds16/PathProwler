#!/bin/bash
# Gobuster Pro - Run Script for Linux/Mac
# This script runs the TUI using the virtual environment

# Colors
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Check if virtual environment exists
if [ ! -f "venv/bin/python" ]; then
    echo -e "${RED}[!] ERROR: Virtual environment not found${NC}"
    echo -e "${RED}[!] Please run the installation script first: ./install.sh${NC}"
    exit 1
fi

# Run the TUI
echo -e "${CYAN}[*] Starting Gobuster Pro TUI...${NC}"
echo ""
./venv/bin/python gobuster_tui.py
