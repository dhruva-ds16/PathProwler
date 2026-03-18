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
	appendStatus := "No"
	if m.appendDomain {
		appendStatus = "Yes"
	}
	
	config := fmt.Sprintf(`
╭─────────────────────────────────────────────────────────────╮
│  🎯 Target:         %-39s │
│  🔍 Mode:           %-39s │
│  🌐 Domain:         %-39s │
│  🔗 Append Domain:  %-39s │
│  ⚡ Threads:        %-39s │
│  📄 Extensions:     %-39s │
│  📚 Wordlist:       %-39s │
╰─────────────────────────────────────────────────────────────╯
`,
		truncate(getValue(m.targetInput.Value()), 39),
		truncate(getValue(m.modeInput.Value(), "dir"), 39),
		truncate(getValue(m.domainInput.Value(), "N/A"), 39),
		truncate(appendStatus, 39),
		truncate(getValue(m.threadsInput.Value(), "50"), 39),
		truncate(getValue(m.extensionsInput.Value(), "None"), 39),
		truncate(getValue(m.wordlistInput.Value(), "raft-large-directories.txt"), 39),
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
