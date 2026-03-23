from pathlib import Path

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def list_dir(path):
    return [p.name for p in Path(path).iterdir()]