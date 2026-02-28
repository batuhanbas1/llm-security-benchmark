def read_file(filename):
    with open("/var/data/" + filename, "r") as f:
        return f.read()