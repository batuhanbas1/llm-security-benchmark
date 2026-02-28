import tempfile

def create_temp():
    temp = tempfile.mktemp()
    with open(temp, "w") as f:
        f.write("data")