import json
import os
import glob

def generate_markdown_report():
    # 1. Find the newest log file in the /logs folder
    list_of_files = glob.glob('logs/*.json')
    if not list_of_files:
        print("❌ No logs found to report on.")
        return

    latest_file = max(list_of_files, key=os.path.getctime)
    
    with open(latest_file, 'r') as f:
        steps = json.load(f)

    # 2. Build the Markdown content
    report_md = f"# 🛡️ VeriTrace Audit Report\n\n"
    report_md += f"**Source File:** `{latest_file}`\n"
    report_md += f"**Final Status:** {'✅ VERIFIED' if steps[-1]['audit_passed'] else '❌ FAILED'}\n\n"
    report_md += "--- \n\n"

    for step in steps:
        report_md += f"### 📍 Attempt {step['attempt']}\n"
        report_md += f"**Reasoning:**\n> {step['reasoning']}\n\n"
        report_md += f"**Answer:** `{step['answer']}`\n"
        report_md += f"**Audit Result:** {'✅ Passed' if step['audit_passed'] else '❌ Rejected'}\n\n"
        report_md += "---\n"

    # 3. Save as a Markdown file
    with open("LATEST_TRACE.md", "w") as f:
        f.write(report_md)
    
    print(f"📄 [REPORTER]: Markdown report generated: LATEST_TRACE.md")

if __name__ == "__main__":
    generate_markdown_report()