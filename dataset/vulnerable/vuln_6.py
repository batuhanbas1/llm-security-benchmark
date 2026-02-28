import subprocess

def list_dir(path):
    subprocess.call("ls " + path, shell=True)