# Directory Naming Convention

Results are now organized by **target domain/IP** instead of timestamps for better organization and easier identification.

## Naming Format

### For Domains
```
gobuster_<domain>
```

**Examples:**
- `http://example.com` → `gobuster_example.com`
- `https://api.example.com` → `gobuster_api.example.com`
- `http://dev.staging.example.com` → `gobuster_dev.staging.example.com`

### For IP Addresses
```
gobuster_<ip_with_underscores>
```

**Examples:**
- `http://192.168.1.100` → `gobuster_192_168_1_100`
- `https://10.0.0.5` → `gobuster_10_0_0_5`
- `http://172.16.0.1:8080` → `gobuster_172_16_0_1`

### Multiple Scans (Same Target)
If you scan the same target multiple times, a counter is appended:

```
gobuster_example.com
gobuster_example.com_1
gobuster_example.com_2
```

## Directory Structure

### Single Target Scan
```
gobuster_example.com/
├── directories.txt
├── files.txt
├── subdomains_dns.txt
├── subdomains_vhost.txt
├── subdomains_all.txt
├── results.json
├── results.csv
├── results.html
└── scan.log
```

### Multiple Targets
```
./
├── gobuster_example.com/
│   ├── directories.txt
│   ├── files.txt
│   └── ...
├── gobuster_api.example.com/
│   ├── directories.txt
│   ├── files.txt
│   └── ...
├── gobuster_192_168_1_100/
│   ├── directories.txt
│   ├── files.txt
│   └── ...
└── gobuster_10_0_0_5/
    ├── directories.txt
    ├── files.txt
    └── ...
```

## Benefits

### ✅ Easy Identification
```bash
# Old way (timestamp-based)
gobuster_results_20260317_174530/  # Which target was this?
gobuster_results_20260317_180245/  # And this?

# New way (domain/IP-based)
gobuster_example.com/              # Clear!
gobuster_192_168_1_100/            # Obvious!
```

### ✅ Better Organization
```bash
# Group by target
ls -d gobuster_example.com*
gobuster_example.com
gobuster_example.com_1
gobuster_example.com_2

# Find specific target results
ls -d gobuster_192_168_1_*
gobuster_192_168_1_100
gobuster_192_168_1_101
```

### ✅ Easier Scripting
```bash
# Process all results for a domain
for dir in gobuster_example.com*; do
  echo "Processing $dir..."
  cat "$dir/subdomains_all.txt"
done

# Compare scans over time
diff gobuster_example.com/directories.txt \
     gobuster_example.com_1/directories.txt
```

### ✅ Quick Access
```bash
# Jump to specific target results
cd gobuster_example.com

# View results
cat subdomains_all.txt
```

## Examples

### CLI Usage
```bash
# Scan example.com
python gobuster_scan.py -u http://example.com -m all -d example.com
# Creates: gobuster_example.com/

# Scan IP address
python gobuster_scan.py -u http://192.168.1.100 -m dir
# Creates: gobuster_192_168_1_100/

# Scan subdomain
python gobuster_scan.py -u http://api.example.com -m files
# Creates: gobuster_api.example.com/

# Second scan of same target
python gobuster_scan.py -u http://example.com -m subdomain -d example.com
# Creates: gobuster_example.com_1/
```

### TUI Usage
The TUI automatically creates directories based on the target URL you enter:

```
Target URL: http://example.com
→ Creates: gobuster_example.com/

Target URL: http://192.168.1.100
→ Creates: gobuster_192_168_1_100/
```

## Special Cases

### Ports
Ports are automatically removed from directory names:

```
http://example.com:8080 → gobuster_example.com
http://192.168.1.100:443 → gobuster_192_168_1_100
```

### Invalid Characters
Invalid filesystem characters are replaced with underscores:

```
http://my-app.example.com → gobuster_my-app.example.com
http://test@example.com → gobuster_test_example.com
```

### Localhost
```
http://localhost → gobuster_localhost
http://127.0.0.1 → gobuster_127_0_0_1
```

## Migration from Old Format

If you have old timestamp-based directories, you can rename them:

```bash
# Manual rename
mv gobuster_results_20260317_174530 gobuster_example.com

# Batch rename (if you know the targets)
mv gobuster_results_20260317_174530 gobuster_example.com
mv gobuster_results_20260317_180245 gobuster_api.example.com
```

## Workflow Examples

### Scanning Multiple Subdomains
```bash
# Scan main domain
python gobuster_scan.py -u http://example.com -m all -d example.com

# Scan discovered subdomains
python gobuster_scan.py -u http://api.example.com -m dir
python gobuster_scan.py -u http://dev.example.com -m dir
python gobuster_scan.py -u http://staging.example.com -m dir

# Results organized by subdomain
ls -d gobuster_*
gobuster_example.com/
gobuster_api.example.com/
gobuster_dev.example.com/
gobuster_staging.example.com/
```

### Scanning IP Range
```bash
# Scan multiple IPs
for ip in 192.168.1.{1..10}; do
  python gobuster_scan.py -u "http://$ip" -m dir
done

# Results organized by IP
ls -d gobuster_192_168_1_*
gobuster_192_168_1_1/
gobuster_192_168_1_2/
gobuster_192_168_1_3/
...
```

### Comparing Scans
```bash
# First scan
python gobuster_scan.py -u http://example.com -m subdomain -d example.com
# Creates: gobuster_example.com/

# Wait some time...

# Second scan
python gobuster_scan.py -u http://example.com -m subdomain -d example.com
# Creates: gobuster_example.com_1/

# Compare results
diff gobuster_example.com/subdomains_all.txt \
     gobuster_example.com_1/subdomains_all.txt
```

### Aggregating Results
```bash
# Combine all subdomain findings for a domain
cat gobuster_example.com*/subdomains_all.txt | \
  grep -v "^#" | \
  sort -u > all_subdomains_example.com.txt

# Count total unique findings
wc -l all_subdomains_example.com.txt
```

## Tips

### 1. Clean Organization
Keep your scan results organized by target:
```bash
mkdir scans
cd scans
python gobuster_scan.py -u http://target1.com -m all -d target1.com
python gobuster_scan.py -u http://target2.com -m all -d target2.com
```

### 2. Archive Old Scans
```bash
# Archive old scans with date
tar -czf example.com_$(date +%Y%m%d).tar.gz gobuster_example.com*
```

### 3. Quick Search
```bash
# Find all results for a domain
find . -name "gobuster_example.com*" -type d

# Search within results
grep -r "admin" gobuster_example.com*/
```

### 4. Cleanup
```bash
# Remove old duplicate scans (keep only latest)
rm -rf gobuster_example.com_[0-9]*

# Keep only the base directory
ls -d gobuster_example.com
```

## Summary

**Old Format:**
```
gobuster_results_20260317_174530/  ❌ Hard to identify
gobuster_results_20260317_180245/  ❌ No context
```

**New Format:**
```
gobuster_example.com/              ✅ Clear target
gobuster_192_168_1_100/            ✅ Easy to find
```

The new naming convention makes it **immediately obvious** which target each directory belongs to, making organization and analysis much easier!
