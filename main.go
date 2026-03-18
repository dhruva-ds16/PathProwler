package main

import (
	"fmt"
	"os"

	tea "github.com/charmbracelet/bubbletea"
)

func main() {
	// Check if feroxbuster is installed
	if !checkFeroxbuster() {
		fmt.Println("❌ feroxbuster not found!")
		fmt.Println("Install: cargo install feroxbuster")
		fmt.Println("Or: https://github.com/epi052/feroxbuster")
		os.Exit(1)
	}

	// Start TUI
	p := tea.NewProgram(initialModel(), tea.WithAltScreen())
	if _, err := p.Run(); err != nil {
		fmt.Printf("Error: %v\n", err)
		os.Exit(1)
	}
}
