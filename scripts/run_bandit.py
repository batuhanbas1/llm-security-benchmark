
import subprocess
import sys
from pathlib import Path


RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_FILE = RESULTS_DIR / "bandit_raw.json"
DATASET_DIR = Path("dataset")


command = [
    sys.executable, "-m", "bandit",
    "-r", str(DATASET_DIR),
    "-f", "json",
    "-o", str(RESULTS_FILE)
]

print("Running Bandit...")


result = subprocess.run(command, check=False)

if result.returncode == 0:
    print("Bandit run completed: No vulnerabilities found.")
else:
    print(f"Bandit run completed with exit code {result.returncode} (Vulnerabilities found or other error).")

print(f"Bandit results saved to {RESULTS_FILE}")