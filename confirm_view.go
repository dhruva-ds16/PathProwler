package main

import (
	"fmt"
	"strings"

	"github.com/charmbracelet/lipgloss"
)

func (m model) confirmView() string {
	var b strings.Builder

	// Title
	title := titleStyle.Render("📋 Confirm Scan Configuration")
	b.WriteString(title)
	b.WriteString("\n\n")

	// Configuration table
	config := fmt.Sprintf(`
╭─────────────────────────────────────────────────────────────╮
│  🎯 Target:      %-42s │
│  🔍 Mode:        %-42s │
│  🌐 Domain:      %-42s │
│  ⚡ Threads:     %-42s │
│  📄 Extensions:  %-42s │
│  📚 Wordlist:    %-42s │
╰─────────────────────────────────────────────────────────────╯
`,
		truncate(getValue(m.targetInput.Value()), 42),
		truncate(getValue(m.modeInput.Value(), "dir"), 42),
		truncate(getValue(m.domainInput.Value(), "N/A"), 42),
		truncate(getValue(m.threadsInput.Value(), "50"), 42),
		truncate(getValue(m.extensionsInput.Value(), "None"), 42),
		truncate(getValue(m.wordlistInput.Value(), "raft-large-directories.txt"), 42),
	)

	b.WriteString(statsStyle.Render(config))
	b.WriteString("\n\n")

	// Instructions
	instructions := lipgloss.NewStyle().
		Foreground(lipgloss.Color("green")).
		Bold(true).
		Render("Press Enter to start scan")
	
	cancel := helpStyle.Render("Esc: Go back • q: Quit")
	
	b.WriteString(instructions)
	b.WriteString("\n")
	b.WriteString(cancel)

	return docStyle.Render(b.String())
}

func getValue(value string, defaultVal ...string) string {
	if value != "" {
		return value
	}
	if len(defaultVal) > 0 {
		return defaultVal[0]
	}
	return ""
}

func truncate(s string, maxLen int) string {
	if len(s) <= maxLen {
		return s
	}
	return s[:maxLen-3] + "..."
}
