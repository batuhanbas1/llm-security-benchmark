import subprocess

def list_directory(path):
    result = subprocess.run(["ls", path], check=True, capture_output=True, text=True)
    return result.stdout