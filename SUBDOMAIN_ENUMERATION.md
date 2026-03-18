# Comprehensive Subdomain Enumeration Guide

PathProwler now includes **dual-technique subdomain enumeration** combining DNS resolution and VHost scanning for maximum coverage.

## Why Two Techniques?

### DNS Resolution
- **What it finds:** Subdomains with actual DNS A/AAAA records
- **Pros:** Finds publicly resolvable subdomains, gets IP addresses
- **Cons:** Misses internal/non-DNS subdomains

### VHost Scanning
- **What it finds:** Virtual hosts configured on the web server
- **Pros:** Finds internal subdomains, dev environments, hidden services
- **Cons:** Requires target URL, may miss external subdomains

### Combined Approach
Using **both techniques** gives you:
- ✅ Public subdomains (DNS)
- ✅ Internal subdomains (VHost)
- ✅ Development environments
- ✅ Hidden services
- ✅ Complete coverage

## Scan Modes

### 1. DNS Only (`-m dns`)
Pure DNS resolution-based enumeration.

```bash
python pathprowler.py -u http://target.com -m dns -d target.com
```

**Output:**
- `subdomains_dns.txt` - Raw DNS results
- Finds: Public subdomains with DNS records

### 2. VHost Only (`-m vhost`)
Pure virtual host scanning.

```bash
python pathprowler.py -u http://target.com -m vhost -d target.com
```

**Output:**
- `vhosts.txt` - Raw VHost results
- Finds: Virtual hosts on the target server

### 3. Comprehensive Subdomain Enumeration (`-m subdomain`)
**RECOMMENDED** - Combines both techniques!

```bash
python pathprowler.py -u http://target.com -m subdomain -d target.com
```

**Output:**
- `subdomains_dns.txt` - DNS results
- `subdomains_vhost.txt` - VHost results
- `subdomains_all.txt` - **Merged & deduplicated results**
- `results.json` - Structured data

**Process:**
1. Runs DNS enumeration
2. Runs VHost enumeration
3. Merges results
4. Deduplicates entries
5. Saves combined list

### 4. Full Reconnaissance (`-m all`)
Everything: directories, files, and comprehensive subdomain enumeration.

```bash
python pathprowler.py -u http://target.com -m all -d target.com -o all
```

## CLI Examples

### Quick Subdomain Discovery
```bash
# Fast scan with 100 threads
python pathprowler.py -u http://target.com -m subdomain -d target.com -t 100
```

### Comprehensive Scan with All Output Formats
```bash
# Get JSON, CSV, HTML reports
python pathprowler.py -u http://target.com -m subdomain -d target.com -o all
```

### Stealth Subdomain Enumeration
```bash
# Slower, less noisy
python pathprowler.py -u http://target.com -m subdomain -d target.com \
  -t 25 \
  --delay 100 \
  --timeout 15
```

### Maximum Speed
```bash
# Aggressive scanning
python pathprowler.py -u http://target.com -m subdomain -d target.com \
  -t 200 \
  --timeout 3
```

### Through Proxy (Burp Suite)
```bash
# Route through proxy for analysis
python pathprowler.py -u http://target.com -m subdomain -d target.com \
  -p http://127.0.0.1:8080
```

## TUI Dashboard Usage

### Start Dashboard
```bash
python pathprowler_tui.py
```

### Configure Subdomain Scan
1. **Target URL**: `http://target.com`
2. **Domain**: `target.com`
3. **Scan Mode**: Select **"Subdomain Enum (DNS + VHost)"**
4. **Threads**: `100` (for speed)
5. Click **"Start Scan"** or press `s`

### Monitor Progress
- **📊 Statistics Panel**: Watch subdomain count increase
- **🔍 DNS Scan Tab**: Live DNS enumeration output
- **🌐 VHost Scan Tab**: Live VHost enumeration output
- **📋 Results Tab**: Combined table of all findings
- **📝 Console Log**: Status messages and completion info

### Export Results
- Press `e` or click **"Export Results"**
- Saves to JSON in results directory

## Output Files

### Directory Structure
```
pathprowler_results_20260317_174530/
├── subdomains_dns.txt       # DNS enumeration results
├── subdomains_vhost.txt     # VHost enumeration results
├── subdomains_all.txt       # ⭐ Merged & deduplicated
├── results.json             # Structured JSON
├── results.csv              # CSV export
├── results.html             # HTML report
└── scan.log                 # Detailed logs
```

### Merged Results Format (`subdomains_all.txt`)
```
# Combined Subdomain Enumeration Results
# Total Unique Subdomains: 47
# Format: subdomain | IP | Source

admin.target.com | 1.2.3.4 | Found
api.target.com | 1.2.3.5 | Found
dev.target.com | 10.0.0.1 | Found
mail.target.com | 1.2.3.6 | Found
staging.target.com | N/A | Found
www.target.com | 1.2.3.4 | Found
```

### JSON Structure
```json
{
  "target": "http://target.com",
  "timestamp": "2026-03-17T17:45:30",
  "results": {
    "subdomains": [
      {
        "path": "www.target.com",
        "status": "Found",
        "size": "1.2.3.4",
        "full_url": "http://www.target.com"
      },
      {
        "path": "dev.target.com",
        "status": "Found",
        "size": "10.0.0.1",
        "full_url": "http://dev.target.com"
      }
    ]
  }
}
```

## Real-World Workflow

### Phase 1: Initial Discovery
```bash
# Quick scan to find low-hanging fruit
python pathprowler.py -u http://target.com -m subdomain -d target.com -t 100 -o json
```

### Phase 2: Analyze Results
```bash
# View unique subdomains
cat pathprowler_results_*/subdomains_all.txt

# Extract just subdomain names
grep -v "^#" pathprowler_results_*/subdomains_all.txt | cut -d'|' -f1 | tr -d ' '

# Count findings
grep -v "^#" pathprowler_results_*/subdomains_all.txt | wc -l
```

### Phase 3: Validate Findings
```bash
# Check which are actually accessible
for sub in $(grep -v "^#" pathprowler_results_*/subdomains_all.txt | cut -d'|' -f1 | tr -d ' '); do
  echo "Testing $sub..."
  curl -I -s "http://$sub" | head -1
done
```

### Phase 4: Deep Dive
```bash
# Scan each discovered subdomain for directories
for sub in $(grep -v "^#" pathprowler_results_*/subdomains_all.txt | cut -d'|' -f1 | tr -d ' '); do
  echo "Scanning $sub..."
  python pathprowler.py -u "http://$sub" -m dir -e php,html,txt
done
```

## Advanced Techniques

### Custom Wordlist
```bash
# Use a different wordlist
python pathprowler.py -u http://target.com -m subdomain -d target.com \
  -w /path/to/custom/wordlists
```

### Combine with Other Tools

#### Export for Aquatone
```bash
# Generate list for screenshot tool
grep -v "^#" pathprowler_results_*/subdomains_all.txt | \
  cut -d'|' -f1 | tr -d ' ' > subdomains.txt
cat subdomains.txt | aquatone
```

#### Export for Nmap
```bash
# Scan all discovered subdomains
grep -v "^#" pathprowler_results_*/subdomains_all.txt | \
  cut -d'|' -f2 | tr -d ' ' | grep -v "N/A" | \
  xargs -I {} nmap -sV -p- {}
```

#### Export for Nuclei
```bash
# Vulnerability scanning
grep -v "^#" pathprowler_results_*/subdomains_all.txt | \
  cut -d'|' -f1 | tr -d ' ' | \
  sed 's/^/http:\/\//' > urls.txt
nuclei -l urls.txt
```

## Performance Tuning

### Fast Network (100+ Mbps)
```bash
python pathprowler.py -u http://target.com -m subdomain -d target.com \
  -t 200 \
  --timeout 3
```

### Slow Network / Rate Limited
```bash
python pathprowler.py -u http://target.com -m subdomain -d target.com \
  -t 25 \
  --timeout 15 \
  --delay 200
```

### Balanced (Default)
```bash
python pathprowler.py -u http://target.com -m subdomain -d target.com \
  -t 50 \
  --timeout 10
```

## Comparison: DNS vs VHost vs Combined

| Aspect | DNS Only | VHost Only | Combined |
|--------|----------|------------|----------|
| **Public Subdomains** | ✅ | ❌ | ✅ |
| **Internal Subdomains** | ❌ | ✅ | ✅ |
| **IP Resolution** | ✅ | ❌ | ✅ |
| **Dev Environments** | ⚠️ | ✅ | ✅ |
| **Speed** | Fast | Medium | Slower |
| **Coverage** | Medium | Medium | **High** |
| **Requires Target URL** | ❌ | ✅ | ✅ |

**Recommendation:** Always use **Combined** (`-m subdomain`) for complete coverage.

## Common Findings

### Typical Subdomains Discovered

**Production:**
- www.target.com
- api.target.com
- cdn.target.com
- static.target.com

**Development:**
- dev.target.com
- staging.target.com
- test.target.com
- uat.target.com

**Infrastructure:**
- mail.target.com
- smtp.target.com
- vpn.target.com
- ftp.target.com

**Admin/Internal:**
- admin.target.com
- portal.target.com
- dashboard.target.com
- internal.target.com

**Services:**
- blog.target.com
- shop.target.com
- support.target.com
- docs.target.com

## Troubleshooting

### No Results Found
```bash
# Verify domain resolves
nslookup target.com

# Try smaller wordlist first
python pathprowler.py -u http://target.com -m dns -d target.com

# Increase timeout
python pathprowler.py -u http://target.com -m subdomain -d target.com --timeout 20
```

### Too Slow
```bash
# Reduce threads
python pathprowler.py -u http://target.com -m subdomain -d target.com -t 25

# Use DNS only (faster)
python pathprowler.py -u http://target.com -m dns -d target.com
```

### Duplicates in Results
The tool automatically deduplicates! Check `subdomains_all.txt` for the clean list.

### VHost Scan Failing
```bash
# Ensure target URL is correct
# VHost requires HTTP/HTTPS target
python pathprowler.py -u https://target.com -m subdomain -d target.com

# Try DNS only if VHost doesn't work
python pathprowler.py -u http://target.com -m dns -d target.com
```

## Security Considerations

### Legal
- ✅ Always get authorization before scanning
- ✅ Subdomain enumeration is detectable
- ✅ May trigger IDS/IPS alerts
- ✅ Respect rate limits

### Ethical
- Don't overwhelm DNS servers
- Use reasonable thread counts
- Add delays for production systems
- Document your findings responsibly

### Operational
- Save all results for reporting
- Validate findings before reporting
- Cross-reference with other tools
- Document methodology

## Integration Examples

### Automation Script
```bash
#!/bin/bash
DOMAIN=$1
OUTPUT_DIR="recon_${DOMAIN}_$(date +%Y%m%d)"

mkdir -p "$OUTPUT_DIR"

echo "[*] Starting subdomain enumeration for $DOMAIN"
python pathprowler.py -u "http://$DOMAIN" -m subdomain -d "$DOMAIN" -o all

echo "[*] Copying results to $OUTPUT_DIR"
cp -r pathprowler_results_*/* "$OUTPUT_DIR/"

echo "[*] Extracting subdomain list"
grep -v "^#" "$OUTPUT_DIR/subdomains_all.txt" | \
  cut -d'|' -f1 | tr -d ' ' > "$OUTPUT_DIR/subdomains.txt"

echo "[*] Complete! Found $(wc -l < "$OUTPUT_DIR/subdomains.txt") subdomains"
```

### CI/CD Pipeline
```yaml
# .github/workflows/recon.yml
name: Subdomain Enumeration
on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Gobuster
        run: |
          python pathprowler.py -u ${{ secrets.TARGET_URL }} \
            -m subdomain -d ${{ secrets.TARGET_DOMAIN }} -o json
      - name: Upload Results
        uses: actions/upload-artifact@v2
        with:
          name: subdomain-results
          path: pathprowler_results_*/
```

## Best Practices

1. **Start with subdomain mode** - Get complete coverage
2. **Save all output formats** - Use `-o all` for flexibility
3. **Validate findings** - Not all results may be accessible
4. **Deduplicate** - Use the merged `subdomains_all.txt` file
5. **Document** - Keep logs and results for reporting
6. **Iterate** - Scan discovered subdomains for directories
7. **Combine tools** - Use with Amass, Subfinder, etc.
8. **Monitor** - Set up regular scans for new subdomains

## Summary

**For maximum subdomain discovery, use:**
```bash
python pathprowler.py -u http://target.com -m subdomain -d target.com -o all
```

This gives you:
- ✅ DNS resolution results
- ✅ VHost enumeration results
- ✅ Merged & deduplicated list
- ✅ JSON, CSV, HTML reports
- ✅ Complete coverage
