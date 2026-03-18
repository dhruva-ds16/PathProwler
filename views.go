package main

import (
	"fmt"
	"strings"

	"github.com/charmbracelet/lipgloss"
)

func (m model) configView() string {
	var b strings.Builder

	// Banner
	banner := lipgloss.NewStyle().
		Bold(true).
		Foreground(lipgloss.Color("cyan")).
		Padding(1, 2).
		Border(lipgloss.DoubleBorder()).
		BorderForeground(lipgloss.Color("cyan")).
		Align(lipgloss.Center).
		Render(asciiArt)

	b.WriteString(banner)
	b.WriteString("\n\n")

	// Title
	title := titleStyle.Render("⚙️  Scan Configuration")
	b.WriteString(title)
	b.WriteString("\n\n")

	// Input fields
	for i := range m.inputs {
		b.WriteString(m.inputs[i].View())
		if i < len(m.inputs)-1 {
			b.WriteRune('\n')
		}
	}

	// Error message
	if m.errorMsg != "" {
		b.WriteString("\n\n")
		b.WriteString(errorStyle.Render("❌ " + m.errorMsg))
	}

	// Instructions
	b.WriteString("\n\n")
	help := helpStyle.Render("Tab/↑↓: Navigate • Enter: Start Scan • Ctrl+C/q: Quit")
	b.WriteString(help)

	return docStyle.Render(b.String())
}

func (m model) scanningView() string {
	var b strings.Builder

	// Title with spinner
	title := titleStyle.Render(fmt.Sprintf("%s Scanning...", m.spinner.View()))
	b.WriteString(title)
	b.WriteString("\n\n")

	// Statistics panel
	stats := m.renderStats()
	b.WriteString(stats)
	b.WriteString("\n\n")

	// Recent results (last 10)
	b.WriteString(subtitleStyle.Render("📋 Recent Findings"))
	b.WriteString("\n\n")

	start := len(m.results) - 10
	if start < 0 {
		start = 0
	}

	for i := start; i < len(m.results); i++ {
		result := m.results[i]
		var style lipgloss.Style
		var icon string

		if result.resultType == "dir" {
			style = dirStyle
			icon = "📁"
		} else {
			style = fileStyle
			icon = "📄"
		}

		line := fmt.Sprintf("%s %s [%d] (%d bytes)",
			icon, result.path, result.statusCode, result.size)
		b.WriteString(style.Render(line))
		b.WriteString("\n")
	}

	// Instructions
	b.WriteString("\n")
	help := helpStyle.Render("v: View All Results • q: Stop & Quit")
	b.WriteString(help)

	return docStyle.Render(b.String())
}

func (m model) resultsView() string {
	var b strings.Builder

	// Title
	title := titleStyle.Render("📊 Scan Results")
	b.WriteString(title)
	b.WriteString("\n\n")

	// Statistics
	stats := m.renderStats()
	b.WriteString(stats)
	b.WriteString("\n\n")

	// Results table
	b.WriteString(subtitleStyle.Render("📋 All Findings"))
	b.WriteString("\n\n")

	// Group by type
	b.WriteString(dirStyle.Render(fmt.Sprintf("📁 Directories (%d)", m.directories)))
	b.WriteString("\n")
	for _, result := range m.results {
		if result.resultType == "dir" {
			line := fmt.Sprintf("  • %s [%d] (%d bytes)",
				result.path, result.statusCode, result.size)
			b.WriteString(dirStyle.Render(line))
			b.WriteString("\n")
		}
	}

	b.WriteString("\n")
	b.WriteString(fileStyle.Render(fmt.Sprintf("📄 Files (%d)", m.files)))
	b.WriteString("\n")
	for _, result := range m.results {
		if result.resultType == "file" {
			line := fmt.Sprintf("  • %s [%d] (%d bytes)",
				result.path, result.statusCode, result.size)
			b.WriteString(fileStyle.Render(line))
			b.WriteString("\n")
		}
	}

	// Instructions
	b.WriteString("\n")
	help := helpStyle.Render("Esc: Back to Config • q: Quit")
	b.WriteString(help)

	return docStyle.Render(b.String())
}

func (m model) renderStats() string {
	stats := fmt.Sprintf(`
╭─────────────────────────────╮
│  📊 Statistics              │
├─────────────────────────────┤
│  📁 Directories: %-10d │
│  📄 Files:       %-10d │
│  📊 Total:       %-10d │
╰─────────────────────────────╯
`, m.directories, m.files, m.totalResults)

	return statsStyle.Render(stats)
}

const asciiArt = `
 ██████╗  █████╗ ████████╗██╗  ██╗██████╗ ██████╗  ██████╗ ██╗    ██╗██╗     ███████╗██████╗ 
 ██╔══██╗██╔══██╗╚══██╔══╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║██║     ██╔════╝██╔══██╗
 ██████╔╝███████║   ██║   ███████║██████╔╝██████╔╝██║   ██║██║ █╗ ██║██║     █████╗  ██████╔╝
 ██╔═══╝ ██╔══██║   ██║   ██╔══██║██╔═══╝ ██╔══██╗██║   ██║██║███╗██║██║     ██╔══╝  ██╔══██╗
 ██║     ██║  ██║   ██║   ██║  ██║██║     ██║  ██║╚██████╔╝╚███╔███╔╝███████╗███████╗██║  ██║
 ╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝  ╚═╝

                    🐾 Prowl through paths and discover hidden treasures 🎯
                                        v3.0 (Go Edition)
`
