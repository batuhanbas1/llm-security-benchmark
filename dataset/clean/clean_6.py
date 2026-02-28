import os

def read_file(base_path, filename):
    safe_path = os.path.join(base_path, filename)
    safe_path = os.path.abspath(safe_path)

    if not safe_path.startswith(os.path.abspath(base_path)):
        raise ValueError("Invalid path")

    with open(safe_path, "r") as f:
        return f.read()