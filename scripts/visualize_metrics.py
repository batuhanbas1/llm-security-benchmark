import os
import pandas as pd
import matplotlib.pyplot as plt


metrics_path = os.path.join(os.path.dirname(__file__), "../results/final_metrics.csv")


df = pd.read_csv(metrics_path)


plt.figure(figsize=(12,6))
plt.bar(df['file_name'], df['bandit_count'], alpha=0.7, label='Bandit')
plt.bar(df['file_name'], df['llm_result'], alpha=0.7, label='LLM')
plt.xticks(rotation=90)
plt.ylabel("Bulunan Vulnerability Sayısı")
plt.title("Bandit vs LLM Sonuçları")
plt.legend()
plt.tight_layout()


output_path = os.path.join(os.path.dirname(__file__), "../results/metrics_summary.png")
plt.savefig(output_path)
plt.show()