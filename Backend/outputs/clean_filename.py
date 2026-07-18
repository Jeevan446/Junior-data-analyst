from pathlib import Path

def clean_filename(filename):
    path = Path(filename)

    name = path.stem
    extension = path.suffix

    clean_name = ""

    for char in name:
        if char.isalnum() or char == "_":
            clean_name += char
        else:
            clean_name += "_"

    return clean_name + extension