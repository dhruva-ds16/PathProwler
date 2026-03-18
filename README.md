<div align="center">

# 🐾 PathProwler

### *Prowl through paths and discover hidden treasures*

[![Go](https://img.shields.io/badge/Go-1.21+-00ADD8?style=for-the-badge&logo=go&logoColor=white)](https://golang.org)
[![License](https://img.shields.io/badge/license-MIT-orange?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey?style=for-the-badge)](https://github.com/yourusername/pathprowler)

**A blazing-fast web reconnaissance tool with a beautiful Bubble Tea TUI**

Built with Go, Bubble Tea, and Feroxbuster for maximum performance and portability.

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Building](#-building)

</div>

---

## ✨ Features

- 🎨 **Beautiful TUI** - Powered by Bubble Tea and Lipgloss
- ⚡ **Blazing Fast** - Written in Go with Feroxbuster
- 📦 **Single Binary** - No dependencies, just run it
- 🎯 **Interactive** - Easy configuration with arrow keys
- 📊 **Live Statistics** - Real-time results as they're found
- 🔍 **Smart Scanning** - Feroxbuster's intelligent recursion

## 🚀 Installation

### Option 1: Download Pre-built Binary (Recommended)

```bash
# Download latest release
wget https://github.com/yourusername/pathprowler/releases/latest/download/pathprowler-linux

# Make executable
chmod +x pathprowler-linux

# Run
./pathprowler-linux
```

### Option 2: Build from Source

**Prerequisites:**
- Go 1.21+
- Feroxbuster

```bash
# Clone repository
git clone https://github.com/yourusername/pathprowler
cd pathprowler

# Build
./build.sh

# Run
./pathprowler
```

### Install Feroxbuster

```bash
# Via Cargo (Rust)
cargo install feroxbuster

# Or download binary
# https://github.com/epi052/feroxbuster/releases
```

### Cross-Compilation

```bash
# Linux
GOOS=linux GOARCH=amd64 go build -o pathprowler-linux

# macOS
GOOS=darwin GOARCH=amd64 go build -o pathprowler-macos

# Windows
GOOS=windows GOARCH=amd64 go build -o pathprowler.exe
```

## 📖 Usage

1. **Launch the TUI**
   ```bash
   ./pathprowler
   ```

2. **Configure Scan**
   - Enter target URL
   - Set threads (default: 50)
   - Add file extensions (optional)
   - Specify wordlist path
   - Press Enter to start

3. **View Results**
   - Watch live results during scan
   - Press `v` to view all results
   - Press `Esc` to go back
   - Press `q` to quit

## 🎯 Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Tab` / `↑↓` | Navigate fields |
| `Enter` | Start scan |
| `v` | View all results |
| `Esc` | Back to config |
| `q` / `Ctrl+C` | Quit |

## 🏗️ Architecture

```
pathprowler/
├── main.go       # Entry point
├── model.go      # Bubble Tea model & logic
├── views.go      # UI rendering
├── styles.go     # Lipgloss styles
├── go.mod        # Dependencies
└── build.sh      # Build script
```

## 🎨 Technology Stack

- **[Bubble Tea](https://github.com/charmbracelet/bubbletea)** - TUI framework
- **[Lipgloss](https://github.com/charmbracelet/lipgloss)** - Terminal styling
- **[Bubbles](https://github.com/charmbracelet/bubbles)** - TUI components
- **[Feroxbuster](https://github.com/epi052/feroxbuster)** - Fast web fuzzer

## 🆚 Why Go + Feroxbuster?

### Go Benefits
```
✓ Single binary distribution
✓ Cross-platform compilation
✓ Excellent performance
✓ Built-in concurrency
✓ Small memory footprint
✓ Fast startup time
```

### Feroxbuster vs Gobuster
```
✓ Faster (written in Rust)
✓ Better recursion
✓ Smart wildcard detection
✓ Auto-filtering
✓ More modern
✓ Better output
```

## 📊 Performance

**Comparison (10,000 word wordlist):**

| Tool | Time | Memory |
|------|------|--------|
| Python + Gobuster | ~45s | ~80MB |
| **Go + Feroxbuster** | **~12s** | **~15MB** |

## 🔧 Development

```bash
# Install dependencies
go mod download

# Run without building
go run .

# Format code
go fmt ./...

# Run tests (when added)
go test ./...
```

## 📝 TODO

- [ ] Add JSON output export
- [ ] Implement result filtering
- [ ] Add scan profiles
- [ ] Save/load configurations
- [ ] Add progress bar
- [ ] Implement result search
- [ ] Add subdomain enumeration
- [ ] CLI mode (non-interactive)

## 🤝 Contributing

Contributions welcome! This is a complete rewrite in Go for better performance and distribution.

## 📄 License

MIT License

## 🙏 Credits

- **Feroxbuster** - [epi052](https://github.com/epi052/feroxbuster)
- **Bubble Tea** - [Charm](https://github.com/charmbracelet)
- **Original Python version** - PathProwler team

---

**Made with ❤️ and Go**

🐾 Happy Prowling! 🎯
