# DNS Subdomain Enumeration - Usage Guide

DNS subdomain enumeration has been added to both the CLI and TUI versions of Gobuster Pro.

## Features

- **Fast DNS resolution** - Uses gobuster's efficient DNS mode
- **Large wordlist** - 110,000 subdomains from SecLists
- **Parallel scanning** - Runs alongside dir/file/vhost scans
- **IP resolution** - Automatically resolves and displays IP addresses
- **Multiple output formats** - JSON, CSV, HTML, TXT

## CLI Usage

### DNS Scan Only
```bash
# Basic DNS enumeration
python gobuster_scan.py -u http://target.com -m dns -d target.com

# Fast DNS scan with 100 threads
python gobuster_scan.py -u http://target.com -m dns -d target.com -t 100

# DNS scan with JSON output
python gobuster_scan.py -u http://target.com -m dns -d target.com -o json
```

### All Scans (Including DNS)
```bash
# Run all scans in parallel (dir + files + vhost + dns)
python gobuster_scan.py -u http://target.com -m all -d target.com

# All scans with custom settings
python gobuster_scan.py -u http://target.com -m all -d target.com \
  -t 100 \
  --timeout 5 \
  -o all
```

### Custom DNS Wordlist
```bash
# Use a smaller wordlist for faster scanning
python gobuster_scan.py -u http://target.com -m dns -d target.com \
  -w /usr/share/wordlists/seclists

# The tool uses: Discovery/DNS/subdomains-top1million-110000.txt
```

## TUI Usage

### Start the Dashboard
```bash
python gobuster_tui.py
```

### Configure DNS Scan
1. **Target URL**: Enter the target (e.g., http://target.com)
2. **Domain**: Enter the domain for DNS scanning (e.g., target.com)
3. **Scan Mode**: Select "DNS Only" or "All"
4. **Threads**: Increase for faster scanning (default: 50)
5. Press **"Start Scan"** or hit `s`

### Monitor Results
- **📋 Results Tab** - See all subdomains in the table
- **🔍 DNS Scan Tab** - Watch live gobuster DNS output
- **📊 Statistics** - Track subdomains found in real-time

## Output Format

### CLI Output
```
gobuster_results_20260317_173045/
├── subdomains.txt       # Raw gobuster DNS output
├── results.json         # Structured JSON with all results
├── results.csv          # CSV export
├── results.html         # HTML report with clickable links
└── scan.log            # Detailed scan log
```

### JSON Structure
```json
{
  "target": "http://target.com",
  "timestamp": "2026-03-17T17:30:45",
  "results": {
    "subdomains": [
      {
        "path": "www.target.com",
        "status": "Found",
        "size": "1.2.3.4",
        "full_url": "http://www.target.com"
      },
      {
        "path": "mail.target.com",
        "status": "Found",
        "size": "5.6.7.8",
        "full_url": "http://mail.target.com"
      }
    ]
  }
}
```

### CSV Format
```csv
Type,Path,Status,IP Address,Full URL
Subdomain,www.target.com,Found,1.2.3.4,http://www.target.com
Subdomain,mail.target.com,Found,5.6.7.8,http://mail.target.com
```

## Performance Tips

### Fast Scan (Quick Discovery)
```bash
# Use fewer threads for stability
python gobuster_scan.py -u http://target.com -m dns -d target.com -t 50
```

### Maximum Speed
```bash
# Increase threads and reduce timeout
python gobuster_scan.py -u http://target.com -m dns -d target.com \
  -t 200 \
  --timeout 3
```

### Comprehensive Scan
```bash
# Use the full 110k wordlist with moderate speed
python gobuster_scan.py -u http://target.com -m dns -d target.com \
  -t 100 \
  --timeout 10
```

## Example Workflow

### 1. Quick Discovery
```bash
# Start with DNS to find subdomains
python gobuster_scan.py -u http://target.com -m dns -d target.com -o json
```

### 2. Analyze Results
```bash
# Check the JSON output
cat gobuster_results_*/results.json | jq '.results.subdomains'
```

### 3. Scan Found Subdomains
```bash
# Use found subdomains as new targets
python gobuster_scan.py -u http://www.target.com -m dir
python gobuster_scan.py -u http://mail.target.com -m dir
```

### 4. Full Reconnaissance
```bash
# Run everything at once
python gobuster_scan.py -u http://target.com -m all -d target.com -o all
```

## Common Subdomains Found

The wordlist typically discovers:
- **www** - Main website
- **mail** - Email server
- **ftp** - File transfer
- **admin** - Admin panel
- **dev** - Development environment
- **staging** - Staging server
- **api** - API endpoint
- **vpn** - VPN gateway
- **portal** - User portal
- **blog** - Blog subdomain

## Troubleshooting

### No Results Found
- Verify the domain is correct (no http://)
- Check DNS resolution: `nslookup target.com`
- Try a smaller wordlist first
- Increase timeout: `--timeout 15`

### Scan Too Slow
- Reduce threads: `-t 25`
- Use smaller wordlist
- Check network connectivity

### Too Many Threads Error
- Reduce threads to 50 or lower
- Some systems limit concurrent DNS queries

## Integration with Other Tools

### Export for Further Analysis
```bash
# Export to JSON for scripting
python gobuster_scan.py -u http://target.com -m dns -d target.com -o json

# Parse with jq
cat gobuster_results_*/results.json | jq -r '.results.subdomains[].path'
```

### Pipe to Other Tools
```bash
# Extract subdomains and scan with nmap
cat gobuster_results_*/subdomains.txt | grep -oE '[a-z0-9.-]+\.[a-z]+' | \
  xargs -I {} nmap -sV {}
```

### Combine with Directory Busting
```bash
# Find subdomains, then scan each
python gobuster_scan.py -u http://target.com -m dns -d target.com -o json

# Extract and scan
for subdomain in $(cat gobuster_results_*/results.json | jq -r '.results.subdomains[].path'); do
  python gobuster_scan.py -u "http://$subdomain" -m dir
done
```

## Wordlist Information

**Default Wordlist**: `Discovery/DNS/subdomains-top1million-110000.txt`
- **Size**: 110,000 subdomains
- **Source**: SecLists by Daniel Miessler
- **Coverage**: Top 1 million subdomains from various sources

**Alternative Wordlists** (in SecLists):
- `subdomains-top1million-5000.txt` - Faster, less comprehensive
- `subdomains-top1million-20000.txt` - Balanced
- `subdomains-top1million-110000.txt` - Most comprehensive (default)

## Best Practices

1. **Start small** - Use 5k wordlist first, then expand
2. **Respect rate limits** - Don't overwhelm DNS servers
3. **Save results** - Always use `-o json` for later analysis
4. **Verify findings** - Check if subdomains are actually accessible
5. **Combine techniques** - Use DNS + VHost + Directory scanning together

## Security Note

Always obtain proper authorization before scanning. DNS enumeration can be detected and may be considered reconnaissance.
