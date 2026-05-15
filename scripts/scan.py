import re
import json
import sys
import os
from datetime import datetime

# Patterns to detect secrets
PATTERNS = {
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "AWS Secret Key": r"(?i)aws.{0,20}secret.{0,20}['\"][0-9a-zA-Z/+]{40}['\"]",
    "API Key": r"(?i)api[_-]?key.{0,10}['\"][a-zA-Z0-9]{20,}['\"]",
    "Password": r"(?i)password\s*=\s*['\"][^'\"]{4,}['\"]",
    "Database URL": r"(?i)(mysql|postgresql|mongodb):\/\/[^\s]+",
    "GitHub Token": r"ghp_[0-9a-zA-Z]{36}",
    "JWT Token": r"eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}",
    "Private Key": r"-----BEGIN (RSA |EC )?PRIVATE KEY-----",
}

def scan_file(filepath):
    findings = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            for line_num, line in enumerate(lines, 1):
                for secret_type, pattern in PATTERNS.items():
                    if re.search(pattern, line):
                        findings.append({
                            "file": filepath,
                            "line": line_num,
                            "type": secret_type,
                            "content": line.strip()
                        })
    except Exception as e:
        print(f"Error scanning {filepath}: {e}")
    return findings

def scan_directory(directory):
    all_findings = []
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules']]
        for file in files:
            if file.endswith(('.py', '.js', '.env', '.txt', '.yaml', '.yml', '.json', '.config')):
                filepath = os.path.join(root, file)
                findings = scan_file(filepath)
                all_findings.extend(findings)
    return all_findings

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    findings = scan_directory(target)
    print(json.dumps({
        "timestamp": datetime.now().isoformat(),
        "target": target,
        "total_findings": len(findings),
        "findings": findings
    }, indent=2))