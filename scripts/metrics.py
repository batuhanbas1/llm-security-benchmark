
import pandas as pd
from pathlib import Path


RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

BANDIT_FILE = RESULTS_DIR / "bandit.csv"
LLM_FILE = RESULTS_DIR / "llm.csv"
OUTPUT_FILE = RESULTS_DIR / "final_metrics.csv"


if not BANDIT_FILE.exists() or not LLM_FILE.exists():
    print("Error: Missing CSV files. Please make sure both parse_bandit.py and run_llm.py have been successfully run.")
    exit(1)


bandit_df = pd.read_csv(BANDIT_FILE)
llm_df = pd.read_csv(LLM_FILE)


if not bandit_df.empty:
    bandit_counts = bandit_df.groupby("file_name").size().reset_index(name="bandit_count")
else:
    
    bandit_counts = pd.DataFrame(columns=["file_name", "bandit_count"])


if not llm_df.empty:
    llm_results = llm_df.groupby("file_name")["llm_result"].max().reset_index()
else:
    llm_results = pd.DataFrame(columns=["file_name", "llm_result"])


merged = pd.merge(bandit_counts, llm_results, on="file_name", how="outer").fillna(0)



tp = ((merged["bandit_count"] > 0) & (merged["llm_result"] == 1)).sum()

fp = ((merged["bandit_count"] == 0) & (merged["llm_result"] == 1)).sum()

fn = ((merged["bandit_count"] > 0) & (merged["llm_result"] == 0)).sum()


precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
total_samples = merged.shape[0]
accuracy = (total_samples - fp - fn) / total_samples if total_samples > 0 else 0.0


print(f"Metrics Evaluation (Total files evaluated: {total_samples})")
print("-" * 40)
print(f"True Positives (TP): {tp}")
print(f"False Positives (FP): {fp}")
print(f"False Negatives (FN): {fn}")
print(f"True Negatives (TN): {total_samples - tp - fp - fn}")
print("-" * 40)
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"Accuracy:  {accuracy:.4f}")


merged.to_csv(OUTPUT_FILE, index=False)
print(f"\nFinal metrics comparison view saved to {OUTPUT_FILE}")