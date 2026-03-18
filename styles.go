package main

import "github.com/charmbracelet/lipgloss"

var (
	// Color palette
	primaryColor   = lipgloss.Color("cyan")
	accentColor    = lipgloss.Color("magenta")
	successColor   = lipgloss.Color("green")
	warningColor   = lipgloss.Color("yellow")
	errorColor     = lipgloss.Color("red")
	mutedColor     = lipgloss.Color("240")
	dirColor       = lipgloss.Color("green")
	fileColor      = lipgloss.Color("yellow")

	// Base styles
	docStyle = lipgloss.NewStyle().
		Padding(1, 2)

	titleStyle = lipgloss.NewStyle().
		Bold(true).
		Foreground(primaryColor).
		Background(lipgloss.Color("235")).
		Padding(0, 1).
		MarginBottom(1)

	subtitleStyle = lipgloss.NewStyle().
		Bold(true).
		Foreground(accentColor).
		MarginTop(1).
		MarginBottom(1)

	helpStyle = lipgloss.NewStyle().
		Foreground(mutedColor).
		Italic(true)

	errorStyle = lipgloss.NewStyle().
		Foreground(errorColor).
		Bold(true)

	// Input styles
	focusedStyle = lipgloss.NewStyle().
		Foreground(primaryColor).
		Bold(true)

	noStyle = lipgloss.NewStyle()

	// Result styles
	dirStyle = lipgloss.NewStyle().
		Foreground(dirColor)

	fileStyle = lipgloss.NewStyle().
		Foreground(fileColor)

	statsStyle = lipgloss.NewStyle().
		Border(lipgloss.RoundedBorder()).
		BorderForeground(primaryColor).
		Padding(0, 1).
		Foreground(primaryColor)

	spinnerStyle = lipgloss.NewStyle().
		Foreground(accentColor)
)
