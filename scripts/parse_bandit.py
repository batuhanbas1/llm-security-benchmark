import json
import os
import pandas as pd

# JSON'u aç
with open("results/bandit_output.json", "r") as f:
    data = json.load(f)

# Bandit'in issue bulduğu dosyaları set içine al
flagged_files = set()

for item in data["results"]:
    filename = item["filename"]
    basename = os.path.basename(filename.replace("\\", "/"))
    flagged_files.add(basename)

# Dataset içindeki tüm dosyaları bul
all_files = []

for root, dirs, files in os.walk("dataset"):
    for file in files:
        if file.endswith(".py"):
            all_files.append(file)

# Sonuç tablosu oluştur
rows = []

for file in all_files:
    if file in flagged_files:
        bandit_result = 1
    else:
        bandit_result = 0

    rows.append({
        "file_name": file,
        "bandit_result": bandit_result
    })

df = pd.DataFrame(rows)
df.to_csv("results/bandit_parsed.csv", index=False)

print("Bandit parse tamamlandı.")