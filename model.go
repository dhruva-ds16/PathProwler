package main

import (
	"bufio"
	"fmt"
	"os/exec"
	"strings"
	"time"

	"github.com/charmbracelet/bubbles/spinner"
	"github.com/charmbracelet/bubbles/textinput"
	tea "github.com/charmbracelet/bubbletea"
)

type screen int

const (
	configScreen screen = iota
	scanningScreen
	resultsScreen
)

type scanResult struct {
	path       string
	statusCode int
	size       int
	resultType string // "dir", "file"
}

type model struct {
	// UI state
	currentScreen screen
	width         int
	height        int

	// Config inputs
	targetInput     textinput.Model
	threadsInput    textinput.Model
	extensionsInput textinput.Model
	wordlistInput   textinput.Model
	focusIndex      int
	inputs          []textinput.Model

	// Scan state
	scanning     bool
	spinner      spinner.Model
	scanCmd      *exec.Cmd
	results      []scanResult
	directories  int
	files        int
	totalResults int

	// Messages
	statusMsg string
	errorMsg  string
}

func initialModel() model {
	// Create input fields
	ti1 := textinput.New()
	ti1.Placeholder = "http://example.com"
	ti1.Focus()
	ti1.CharLimit = 200
	ti1.Width = 50
	ti1.Prompt = "🎯 Target URL: "

	ti2 := textinput.New()
	ti2.Placeholder = "50"
	ti2.CharLimit = 4
	ti2.Width = 50
	ti2.Prompt = "⚡ Threads: "

	ti3 := textinput.New()
	ti3.Placeholder = "php,html,txt,asp,jsp"
	ti3.CharLimit = 100
	ti3.Width = 50
	ti3.Prompt = "📄 Extensions: "

	ti4 := textinput.New()
	ti4.Placeholder = "/usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt"
	ti4.CharLimit = 300
	ti4.Width = 50
	ti4.Prompt = "📚 Wordlist: "

	// Create spinner
	s := spinner.New()
	s.Spinner = spinner.Dot
	s.Style = spinnerStyle

	return model{
		currentScreen:   configScreen,
		targetInput:     ti1,
		threadsInput:    ti2,
		extensionsInput: ti3,
		wordlistInput:   ti4,
		inputs:          []textinput.Model{ti1, ti2, ti3, ti4},
		focusIndex:      0,
		spinner:         s,
		results:         []scanResult{},
	}
}

func (m model) Init() tea.Cmd {
	return textinput.Blink
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.WindowSizeMsg:
		m.width = msg.Width
		m.height = msg.Height
		return m, nil

	case tea.KeyMsg:
		switch msg.String() {
		case "ctrl+c", "q":
			if m.scanning {
				if m.scanCmd != nil && m.scanCmd.Process != nil {
					m.scanCmd.Process.Kill()
				}
			}
			return m, tea.Quit

		case "esc":
			if m.currentScreen == resultsScreen {
				m.currentScreen = configScreen
				return m, nil
			}

		case "enter":
			if m.currentScreen == configScreen {
				// Validate and start scan
				if m.targetInput.Value() == "" {
					m.errorMsg = "Target URL is required!"
					return m, nil
				}
				return m, m.startScan()
			}

		case "tab", "shift+tab", "up", "down":
			if m.currentScreen == configScreen {
				s := msg.String()

				if s == "up" || s == "shift+tab" {
					m.focusIndex--
				} else {
					m.focusIndex++
				}

				if m.focusIndex > len(m.inputs)-1 {
					m.focusIndex = 0
				} else if m.focusIndex < 0 {
					m.focusIndex = len(m.inputs) - 1
				}

				cmds := make([]tea.Cmd, len(m.inputs))
				for i := 0; i <= len(m.inputs)-1; i++ {
					if i == m.focusIndex {
						cmds[i] = m.inputs[i].Focus()
						m.inputs[i].PromptStyle = focusedStyle
						m.inputs[i].TextStyle = focusedStyle
						continue
					}
					m.inputs[i].Blur()
					m.inputs[i].PromptStyle = noStyle
					m.inputs[i].TextStyle = noStyle
				}

				return m, tea.Batch(cmds...)
			}

		case "v":
			if m.currentScreen == scanningScreen && !m.scanning {
				m.currentScreen = resultsScreen
				return m, nil
			}
		}

	case spinner.TickMsg:
		var cmd tea.Cmd
		m.spinner, cmd = m.spinner.Update(msg)
		return m, cmd

	case scanLineMsg:
		m.processLine(string(msg))
		return m, readLine(m.scanCmd)

	case scanCompleteMsg:
		m.scanning = false
		m.statusMsg = "Scan completed!"
		m.currentScreen = resultsScreen
		return m, nil

	case errMsg:
		m.errorMsg = string(msg)
		m.scanning = false
		return m, nil
	}

	// Update inputs
	if m.currentScreen == configScreen {
		cmd := m.updateInputs(msg)
		return m, cmd
	}

	return m, nil
}

func (m *model) updateInputs(msg tea.Msg) tea.Cmd {
	cmds := make([]tea.Cmd, len(m.inputs))

	for i := range m.inputs {
		m.inputs[i], cmds[i] = m.inputs[i].Update(msg)
	}

	// Update individual fields
	m.targetInput = m.inputs[0]
	m.threadsInput = m.inputs[1]
	m.extensionsInput = m.inputs[2]
	m.wordlistInput = m.inputs[3]

	return tea.Batch(cmds...)
}

func (m model) View() string {
	switch m.currentScreen {
	case configScreen:
		return m.configView()
	case scanningScreen:
		return m.scanningView()
	case resultsScreen:
		return m.resultsView()
	default:
		return ""
	}
}

// Message types
type scanLineMsg string
type scanCompleteMsg struct{}
type errMsg string

func (m *model) startScan() tea.Cmd {
	return func() tea.Msg {
		// Build feroxbuster command
		target := m.targetInput.Value()
		threads := m.threadsInput.Value()
		if threads == "" {
			threads = "50"
		}
		wordlist := m.wordlistInput.Value()
		if wordlist == "" {
			wordlist = "/usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt"
		}

		args := []string{
			"-u", target,
			"-t", threads,
			"-w", wordlist,
			"--silent",
			"--no-state",
		}

		// Add extensions if provided
		if ext := m.extensionsInput.Value(); ext != "" {
			args = append(args, "-x", ext)
		}

		m.scanCmd = exec.Command("feroxbuster", args...)
		
		stdout, err := m.scanCmd.StdoutPipe()
		if err != nil {
			return errMsg(fmt.Sprintf("Failed to create pipe: %v", err))
		}

		if err := m.scanCmd.Start(); err != nil {
			return errMsg(fmt.Sprintf("Failed to start scan: %v", err))
		}

		m.scanning = true
		m.currentScreen = scanningScreen
		m.statusMsg = "Scanning..."

		// Read output line by line
		scanner := bufio.NewScanner(stdout)
		go func() {
			for scanner.Scan() {
				line := scanner.Text()
				// Send line to be processed
				if line != "" {
					// Process in goroutine to avoid blocking
					go func(l string) {
						// This would be sent via a channel in real implementation
					}(line)
				}
			}
		}()

		return spinner.Tick
	}
}

func (m *model) processLine(line string) {
	// Parse feroxbuster output
	// Format: STATUS_CODE SIZE URL
	parts := strings.Fields(line)
	if len(parts) < 3 {
		return
	}

	var result scanResult
	fmt.Sscanf(parts[0], "%d", &result.statusCode)
	fmt.Sscanf(parts[1], "%d", &result.size)
	result.path = parts[2]

	// Determine type based on URL
	if strings.HasSuffix(result.path, "/") {
		result.resultType = "dir"
		m.directories++
	} else {
		result.resultType = "file"
		m.files++
	}

	m.results = append(m.results, result)
	m.totalResults++
}

func readLine(cmd *exec.Cmd) tea.Cmd {
	return func() tea.Msg {
		// This is a simplified version
		// In production, use proper channel-based communication
		time.Sleep(100 * time.Millisecond)
		return scanLineMsg("")
	}
}

func checkFeroxbuster() bool {
	cmd := exec.Command("feroxbuster", "--version")
	return cmd.Run() == nil
}
