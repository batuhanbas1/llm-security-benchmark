import subprocess

subprocess.run([
    "bandit",
    "-r",
    "dataset/",
    "-f",
    "json",
    "-o",
    "results/bandit_output.json"
])