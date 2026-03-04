import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

metrics_path = os.path.join(os.path.dirname(__file__), "../results/final_metrics.csv")

df = pd.read_csv(metrics_path)

plt.figure(figsize=(14, 7))

x = np.arange(len(df['file_name']))
width = 0.35

plt.bar(x - width/2, df['bandit_count'], width, alpha=0.85, color='#1f77b4', label='Bandit')
plt.bar(x + width/2, df['llm_result'], width, alpha=0.85, color='#ff7f0e', label='LLM')

plt.xticks(x, df['file_name'], rotation=90, fontsize=10)
plt.ylabel("Tespit Edilen Zafiyet Sayısı")
plt.title("Bandit vs LLM Güvenlik Analizi Karşılaştırması")

plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.legend()
plt.tight_layout()

output_path = os.path.join(os.path.dirname(__file__), "../results/metrics_summary.png")
plt.savefig(output_path)
plt.show()