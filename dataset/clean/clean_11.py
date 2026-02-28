import tempfile

def create_temp_file():
    with tempfile.NamedTemporaryFile(delete=True) as tmp:
        tmp.write(b"secure data")
        tmp.flush()
        return tmp.name