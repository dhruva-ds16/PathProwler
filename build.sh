#!/bin/bash
# PathProwler Go - Build Script

echo "🐾 Building PathProwler (Go Edition)..."
echo ""

# Check if Go is installed
if ! command -v go &> /dev/null; then
    echo "❌ Go not found! Please install Go 1.21+"
    exit 1
fi

# Get dependencies
echo "📦 Downloading dependencies..."
go mod download
go mod tidy

# Build for current platform
echo "🔨 Building..."
go build -o pathprowler .

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Build successful!"
    echo ""
    echo "Run with: ./pathprowler"
    echo ""
    
    # Make executable
    chmod +x pathprowler
else
    echo ""
    echo "❌ Build failed!"
    exit 1
fi
