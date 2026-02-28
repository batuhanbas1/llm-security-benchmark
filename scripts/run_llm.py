
import os
import csv
from pathlib import Path
from dotenv import load_dotenv
import openai


load_dotenv()


DATASET_DIR = Path("dataset")
CLEAN_DIR = DATASET_DIR / "clean"
VULN_DIR = DATASET_DIR / "vulnerable"
RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_FILE = RESULTS_DIR / "llm.csv"

def ask_llm(code_snippet: str) -> int:
    



    prompt = f"Analyze the following Python code for security vulnerabilities. Respond with only 1 (vulnerable) or 0 (safe).\n\n{code_snippet}"
    
    try:
        
        if hasattr(openai, "OpenAI"):
            
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            answer = response.choices[0].message.content.strip()
        else:
            
            openai.api_key = os.getenv("OPENAI_API_KEY")
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            answer = response.choices[0].message.content.strip()
            
        return 1 if "1" in answer else 0
        
    except Exception as e:
        print("LLM request failed:", e)
        
        return 0

with open(RESULTS_FILE, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    
    writer.writerow(["file_name", "llm_result"])
    
    
    for folder in [CLEAN_DIR, VULN_DIR]:
        if not folder.exists():
            print(f"Warning: Directory {folder} does not exist. Skipping.")
            continue
            
        
        for file_path in folder.glob("*.py"):
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()
            
            result = ask_llm(code)
            print(f"{file_path.name}: {result}")
            
            writer.writerow([file_path.name, result])

print(f"LLM analysis saved to {RESULTS_FILE}")