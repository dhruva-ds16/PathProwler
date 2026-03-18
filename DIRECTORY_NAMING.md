# Directory Naming Convention

Results are now organized by **target domain/IP** instead of timestamps for better organization and easier identification.

## Naming Format

### For Domains
```
pathprowler_<domain>
```

**Examples:**
- `http://example.com` → `pathprowler_example.com`
- `https://api.example.com` → `pathprowler_api.example.com`
- `http://dev.staging.example.com` → `pathprowler_dev.staging.example.com`

### For IP Addresses
```
pathprowler_<ip_with_underscores>
```

**Examples:**
- `http://192.168.1.100` → `pathprowler_192_168_1_100`
- `https://10.0.0.5` → `pathprowler_10_0_0_5`
- `http://172.16.0.1:8080` → `pathprowler_172_16_0_1`

### Multiple Scans (Same Target)
If you scan the same target multiple times, a counter is appended:

```
pathprowler_example.com
pathprowler_example.com_1
pathprowler_example.com_2
```

## Directory Structure

### Single Target Scan
```
pathprowler_example.com/
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
├── pathprowler_example.com/
│   ├── directories.txt
│   ├── files.txt
│   └── ...
├── pathprowler_api.example.com/
│   ├── directories.txt
│   ├── files.txt
│   └── ...
├── pathprowler_192_168_1_100/
│   ├── directories.txt
│   ├── files.txt
│   └── ...
└── pathprowler_10_0_0_5/
    ├── directories.txt
    ├── files.txt
    └── ...
```

## Benefits

### ✅ Easy Identification
```bash
# Old way (timestamp-based)
pathprowler_results_20260317_174530/  # Which target was this?
pathprowler_results_20260317_180245/  # And this?

# New way (domain/IP-based)
pathprowler_example.com/              # Clear!
pathprowler_192_168_1_100/            # Obvious!
```

### ✅ Better Organization
```bash
# Group by target
ls -d pathprowler_example.com*
pathprowler_example.com
pathprowler_example.com_1
pathprowler_example.com_2

# Find specific target results
ls -d pathprowler_192_168_1_*
pathprowler_192_168_1_100
pathprowler_192_168_1_101
```

### ✅ Easier Scripting
```bash
# Process all results for a domain
for dir in pathprowler_example.com*; do
  echo "Processing $dir..."
  cat "$dir/subdomains_all.txt"
done

# Compare scans over time
diff pathprowler_example.com/directories.txt \
     pathprowler_example.com_1/directories.txt
```

### ✅ Quick Access
```bash
# Jump to specific target results
cd pathprowler_example.com

# View results
cat subdomains_all.txt
```

## Examples

### CLI Usage
```bash
# Scan example.com
python pathprowler.py -u http://example.com -m all -d example.com
# Creates: pathprowler_example.com/

# Scan IP address
python pathprowler.py -u http://192.168.1.100 -m dir
# Creates: pathprowler_192_168_1_100/

# Scan subdomain
python pathprowler.py -u http://api.example.com -m files
# Creates: pathprowler_api.example.com/

# Second scan of same target
python pathprowler.py -u http://example.com -m subdomain -d example.com
# Creates: pathprowler_example.com_1/
```

### TUI Usage
The TUI automatically creates directories based on the target URL you enter:

```
Target URL: http://example.com
→ Creates: pathprowler_example.com/

Target URL: http://192.168.1.100
→ Creates: pathprowler_192_168_1_100/
```

## Special Cases

### Ports
Ports are automatically removed from directory names:

```
http://example.com:8080 → pathprowler_example.com
http://192.168.1.100:443 → pathprowler_192_168_1_100
```

### Invalid Characters
Invalid filesystem characters are replaced with underscores:

```
http://my-app.example.com → pathprowler_my-app.example.com
http://test@example.com → pathprowler_test_example.com
```

### Localhost
```
http://localhost → pathprowler_localhost
http://127.0.0.1 → pathprowler_127_0_0_1
```

## Migration from Old Format

If you have old timestamp-based directories, you can rename them:

```bash
# Manual rename
mv pathprowler_results_20260317_174530 pathprowler_example.com

# Batch rename (if you know the targets)
mv pathprowler_results_20260317_174530 pathprowler_example.com
mv pathprowler_results_20260317_180245 pathprowler_api.example.com
```

## Workflow Examples

### Scanning Multiple Subdomains
```bash
# Scan main domain
python pathprowler.py -u http://example.com -m all -d example.com

# Scan discovered subdomains
python pathprowler.py -u http://api.example.com -m dir
python pathprowler.py -u http://dev.example.com -m dir
python pathprowler.py -u http://staging.example.com -m dir

# Results organized by subdomain
ls -d pathprowler_*
pathprowler_example.com/
pathprowler_api.example.com/
pathprowler_dev.example.com/
pathprowler_staging.example.com/
```

### Scanning IP Range
```bash
# Scan multiple IPs
for ip in 192.168.1.{1..10}; do
  python pathprowler.py -u "http://$ip" -m dir
done

# Results organized by IP
ls -d pathprowler_192_168_1_*
pathprowler_192_168_1_1/
pathprowler_192_168_1_2/
pathprowler_192_168_1_3/
...
```

### Comparing Scans
```bash
# First scan
python pathprowler.py -u http://example.com -m subdomain -d example.com
# Creates: pathprowler_example.com/

# Wait some time...

# Second scan
python pathprowler.py -u http://example.com -m subdomain -d example.com
# Creates: pathprowler_example.com_1/

# Compare results
diff pathprowler_example.com/subdomains_all.txt \
     pathprowler_example.com_1/subdomains_all.txt
```

### Aggregating Results
```bash
# Combine all subdomain findings for a domain
cat pathprowler_example.com*/subdomains_all.txt | \
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
python pathprowler.py -u http://target1.com -m all -d target1.com
python pathprowler.py -u http://target2.com -m all -d target2.com
```

### 2. Archive Old Scans
```bash
# Archive old scans with date
tar -czf example.com_$(date +%Y%m%d).tar.gz pathprowler_example.com*
```

### 3. Quick Search
```bash
# Find all results for a domain
find . -name "pathprowler_example.com*" -type d

# Search within results
grep -r "admin" pathprowler_example.com*/
```

### 4. Cleanup
```bash
# Remove old duplicate scans (keep only latest)
rm -rf pathprowler_example.com_[0-9]*

# Keep only the base directory
ls -d pathprowler_example.com
```

## Summary

**Old Format:**
```
pathprowler_results_20260317_174530/  ❌ Hard to identify
pathprowler_results_20260317_180245/  ❌ No context
```

**New Format:**
```
pathprowler_example.com/              ✅ Clear target
pathprowler_192_168_1_100/            ✅ Easy to find
```

The new naming convention makes it **immediately obvious** which target each directory belongs to, making organization and analysis much easier!
