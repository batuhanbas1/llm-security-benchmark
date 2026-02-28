
import json
import csv
from pathlib import Path


RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
INPUT_FILE = RESULTS_DIR / "bandit_raw.json"
OUTPUT_FILE = RESULTS_DIR / "bandit.csv"


if not INPUT_FILE.exists():
    print(f"Error: {INPUT_FILE} not found. Please run scripts/run_bandit.py first.")
    exit(1)


with open(INPUT_FILE, "r", encoding="utf-8") as f:
    try:
        data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: {INPUT_FILE} contains invalid JSON. It might be empty or corrupted.")
        data = {}


with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    
    writer.writerow(["file_name", "line_number", "issue_text", "severity", "confidence"])
    
    
    for result in data.get("results", []):
        full_filename = result.get("filename", "")
        
        file_name = Path(full_filename).name
        
        line_number = result.get("line_number", "")
        issue_text = result.get("issue_text", "")
        severity = result.get("issue_severity", "")
        confidence = result.get("issue_confidence", "")
        
        writer.writerow([file_name, line_number, issue_text, severity, confidence])

print(f"Bandit CSV saved to {OUTPUT_FILE}")