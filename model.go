package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
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
	confirmScreen
	scanningScreen
	resultsScreen
)

type scanMode string

const (
	modeDirs      scanMode = "dir"
	modeVHost     scanMode = "vhost"
	modeDNS       scanMode = "dns"
	modeAll       scanMode = "all"
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
	modeInput       textinput.Model
	domainInput     textinput.Model
	threadsInput    textinput.Model
	extensionsInput textinput.Model
	wordlistInput   textinput.Model
	appendInput     textinput.Model
	focusIndex      int
	inputs          []textinput.Model

	// Scan state
	scanning      bool
	spinner       spinner.Model
	scanCmd       *exec.Cmd
	results       []scanResult
	directories   int
	files         int
	vhosts        int
	subdomains    int
	totalResults  int
	wordlistSize  int
	wordsScanned  int
	selectedMode  scanMode
	appendDomain  bool

	// Messages
	statusMsg string
	errorMsg  string
}

func initialModel() model {
	// Create input fields with proper settings
	ti1 := textinput.New()
	ti1.Placeholder = "http://example.com"
	ti1.Focus()
	ti1.CharLimit = 200
	ti1.Width = 60
	ti1.Prompt = "🎯 Target URL: "
	ti1.PromptStyle = focusedStyle
	ti1.TextStyle = focusedStyle

	ti2 := textinput.New()
	ti2.Placeholder = "dir (dir/vhost/dns/all)"
	ti2.CharLimit = 10
	ti2.Width = 60
	ti2.Prompt = "🔍 Scan Mode: "

	ti3 := textinput.New()
	ti3.Placeholder = "example.com (for vhost/dns)"
	ti3.CharLimit = 100
	ti3.Width = 60
	ti3.Prompt = "🌐 Domain: "

	ti4 := textinput.New()
	ti4.Placeholder = "50 (default)"
	ti4.CharLimit = 4
	ti4.Width = 60
	ti4.Prompt = "⚡ Threads: "

	ti5 := textinput.New()
	ti5.Placeholder = "php,html,txt (optional)"
	ti5.CharLimit = 100
	ti5.Width = 60
	ti5.Prompt = "📄 Extensions: "

	ti6 := textinput.New()
	ti6.Placeholder = "/usr/share/seclists/Discovery/Web-Content/raft-large-directories.txt"
	ti6.CharLimit = 300
	ti6.Width = 60
	ti6.Prompt = "📚 Wordlist: "

	ti7 := textinput.New()
	ti7.Placeholder = "no (yes/no)"
	ti7.CharLimit = 3
	ti7.Width = 60
	ti7.Prompt = "🔗 Append Domain: "

	// Create spinner
	s := spinner.New()
	s.Spinner = spinner.Dot
	s.Style = spinnerStyle

	return model{
		currentScreen:   configScreen,
		targetInput:     ti1,
		modeInput:       ti2,
		domainInput:     ti3,
		threadsInput:    ti4,
		extensionsInput: ti5,
		wordlistInput:   ti6,
		appendInput:     ti7,
		inputs:          []textinput.Model{ti1, ti2, ti3, ti4, ti5, ti6, ti7},
		focusIndex:      0,
		spinner:         s,
		results:         []scanResult{},
		selectedMode:    modeDirs,
		appendDomain:    false,
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
				// Clear any previous error
				m.errorMsg = ""
				
				// Validate inputs
				target := m.targetInput.Value()
				if target == "" {
					m.errorMsg = "Target URL is required!"
					return m, nil
				}
				
				// Validate mode
				mode := m.modeInput.Value()
				if mode == "" {
					mode = "dir"
				}
				m.selectedMode = scanMode(mode)
				
				// Check append domain setting
				appendVal := strings.ToLower(m.appendInput.Value())
				m.appendDomain = (appendVal == "yes" || appendVal == "y")
				
				// Check domain for vhost/dns modes or append domain
				if (mode == "vhost" || mode == "dns" || mode == "all" || m.appendDomain) && m.domainInput.Value() == "" {
					m.errorMsg = "Domain is required for vhost/dns/all modes or when appending domain!"
					return m, nil
				}
				
				// Go to confirmation screen
				m.currentScreen = confirmScreen
				return m, nil
			}
			
			if m.currentScreen == confirmScreen {
				// Start the scan
				m.scanning = true
				m.currentScreen = scanningScreen
				return m, tea.Batch(m.spinner.Tick, tickCmd(), m.startScan())
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
			if m.currentScreen == scanningScreen {
				m.currentScreen = resultsScreen
				return m, nil
			}
		}

	case spinner.TickMsg:
		var cmd tea.Cmd
		m.spinner, cmd = m.spinner.Update(msg)
		if m.scanning {
			return m, cmd
		}
		return m, nil

	case scanProgressMsg:
		// Periodic refresh during scan
		if m.scanning {
			return m, tickCmd()
		}
		return m, nil

	case errMsg:
		m.errorMsg = msg.msg
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

	// Only update the focused input
	m.inputs[m.focusIndex], cmds[m.focusIndex] = m.inputs[m.focusIndex].Update(msg)

	// Sync back to individual fields
	m.targetInput = m.inputs[0]
	m.modeInput = m.inputs[1]
	m.domainInput = m.inputs[2]
	m.threadsInput = m.inputs[3]
	m.extensionsInput = m.inputs[4]
	m.wordlistInput = m.inputs[5]
	m.appendInput = m.inputs[6]

	return tea.Batch(cmds...)
}

func (m model) View() string {
	switch m.currentScreen {
	case configScreen:
		return m.configView()
	case confirmScreen:
		return m.confirmView()
	case scanningScreen:
		return m.scanningView()
	case resultsScreen:
		return m.resultsView()
	default:
		return ""
	}
}

// Message types
type scanLineMsg struct {
	line string
}
type scanCompleteMsg struct{}
type scanProgressMsg struct{}
type errMsg struct {
	msg string
}

func (m *model) startScan() tea.Cmd {
	return func() tea.Msg {
		// Get config values
		target := m.targetInput.Value()
		domain := m.domainInput.Value()
		threads := m.threadsInput.Value()
		if threads == "" {
			threads = "50"
		}
		wordlist := m.wordlistInput.Value()
		if wordlist == "" {
			wordlist = "/usr/share/seclists/Discovery/Web-Content/raft-large-directories.txt"
		}

		// Count wordlist size for progress
		m.wordlistSize = countLines(wordlist)

		var args []string
		
		// Build command based on mode
		switch m.selectedMode {
		case modeVHost:
			args = []string{
				"vhost",
				"-u", target,
				"-w", wordlist,
				"-t", threads,
				"--domain", domain,
			}
		case modeDNS:
			args = []string{
				"dns",
				"-d", domain,
				"-w", wordlist,
				"-t", threads,
			}
		default: // dir or all
			args = []string{
				"dir",
				"-u", target,
				"-w", wordlist,
				"-t", threads,
				"--silent",
				"--no-state",
			}
			
			// Add extensions if provided
			if ext := m.extensionsInput.Value(); ext != "" {
				args = append(args, "-x", ext)
			}
		}

		m.scanCmd = exec.Command("feroxbuster", args...)
		
		stdout, err := m.scanCmd.StdoutPipe()
		if err != nil {
			return errMsg{msg: fmt.Sprintf("Failed to create pipe: %v", err)}
		}

		if err := m.scanCmd.Start(); err != nil {
			return errMsg{msg: fmt.Sprintf("Failed to start scan: %v", err)}
		}

		m.statusMsg = "Scanning..."

		// Start reading output in background
		go m.readScanOutput(stdout)

		return spinner.Tick
	}
}

func (m *model) readScanOutput(stdout io.ReadCloser) {
	scanner := bufio.NewScanner(stdout)
	for scanner.Scan() {
		line := scanner.Text()
		if line != "" {
			m.wordsScanned++
			m.processLine(line)
		}
	}
	
	// Wait for command to finish
	if m.scanCmd != nil {
		m.scanCmd.Wait()
	}
	
	m.scanning = false
	m.statusMsg = "Scan complete!"
}

func countLines(filepath string) int {
	// Try wc command (Unix/Linux)
	file, err := exec.Command("wc", "-l", filepath).Output()
	if err == nil {
		var count int
		fmt.Sscanf(string(file), "%d", &count)
		return count
	}
	
	// Fallback: count manually
	f, err := os.Open(filepath)
	if err != nil {
		return 0
	}
	defer f.Close()
	
	count := 0
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		count++
	}
	return count
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

	// Append domain if enabled
	if m.appendDomain && m.selectedMode == modeDirs {
		domain := m.domainInput.Value()
		if domain != "" {
			// Extract just the path from the URL
			if strings.Contains(result.path, "://") {
				urlParts := strings.SplitN(result.path, "://", 2)
				if len(urlParts) == 2 {
					pathParts := strings.SplitN(urlParts[1], "/", 2)
					if len(pathParts) == 2 {
						result.path = urlParts[0] + "://" + domain + "/" + pathParts[1]
					}
				}
			}
		}
	}

	// Determine type based on mode and URL
	switch m.selectedMode {
	case modeVHost:
		result.resultType = "vhost"
		m.vhosts++
	case modeDNS:
		result.resultType = "subdomain"
		m.subdomains++
	default:
		// Determine type based on URL
		if strings.HasSuffix(result.path, "/") {
			result.resultType = "dir"
			m.directories++
		} else {
			result.resultType = "file"
			m.files++
		}
	}

	m.results = append(m.results, result)
	m.totalResults++
}

// Periodic UI refresh during scanning
func tickCmd() tea.Cmd {
	return tea.Tick(time.Millisecond*100, func(t time.Time) tea.Msg {
		return scanProgressMsg{}
	})
}

func checkFeroxbuster() bool {
	cmd := exec.Command("feroxbuster", "--version")
	return cmd.Run() == nil
}
