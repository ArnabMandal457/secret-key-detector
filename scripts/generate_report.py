import json
import sys
from datetime import datetime

def generate_html(scan_results):
    findings = scan_results.get("findings", [])
    total = scan_results.get("total_findings", 0)
    timestamp = scan_results.get("timestamp", "")
    
    severity_color = "#e74c3c" if total > 0 else "#2ecc71"
    status_text = f"⚠️ {total} SECRET(S) FOUND" if total > 0 else "✅ NO SECRETS FOUND"

    rows = ""
    for f in findings:
        rows += f"""
        <tr>
            <td>{f['file']}</td>
            <td>{f['line']}</td>
            <td><span class="badge">{f['type']}</span></td>
            <td><code>{f['content'][:80]}</code></td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Secret Key Detector Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #0d1117; color: #c9d1d9; padding: 30px; }}
        h1 {{ color: #58a6ff; }}
        .status {{ font-size: 24px; font-weight: bold; color: {severity_color}; margin: 20px 0; }}
        .meta {{ color: #8b949e; margin-bottom: 30px; }}
        table {{ width: 100%; border-collapse: collapse; background: #161b22; }}
        th {{ background: #21262d; padding: 12px; text-align: left; color: #58a6ff; }}
        td {{ padding: 10px; border-bottom: 1px solid #21262d; }}
        code {{ background: #21262d; padding: 2px 6px; border-radius: 4px; color: #ff7b72; }}
        .badge {{ background: #da3633; color: white; padding: 2px 8px; border-radius: 10px; font-size: 12px; }}
        .no-findings {{ color: #2ecc71; font-size: 18px; margin-top: 30px; }}
    </style>
</head>
<body>
    <h1>🔐 Secret Key Detector</h1>
    <div class="status">{status_text}</div>
    <div class="meta">
        <p>📅 Scan Time: {timestamp}</p>
        <p>🎯 Target: {scan_results.get('target', '')}</p>
    </div>
    {'<table><tr><th>File</th><th>Line</th><th>Type</th><th>Content</th></tr>' + rows + '</table>' if total > 0 else '<p class="no-findings">✅ Your code is clean. No secrets detected.</p>'}
</body>
</html>"""
    return html

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    with open(input_file, 'r') as f:
        scan_results = json.load(f)
    
    html = generate_html(scan_results)
    
    with open(output_file, 'w') as f:
        f.write(html)
    
    print(f"Report generated: {output_file}")