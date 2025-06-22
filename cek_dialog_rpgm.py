import zipfile
import json
import re

def is_dialog_rpgm(line):
    # Kode deteksi dialog (mirip filter kamu!)
    if not isinstance(line, str): return False
    s = line.strip()
    # Berisi huruf dan agak panjang, bukan tag kode saja
    if re.search(r'[a-zA-Z]', s) and len(s) > 3 and not re.match(r'^<[^>]+>$', s):
        return True
    return False

def scan_zip_for_dialogs(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        dialog_files = []
        for fname in zipf.namelist():
            if not fname.lower().endswith('.json'):
                continue
            try:
                content = zipf.read(fname).decode('utf-8')
                data = json.loads(content)
                found = False
                # Cek jika ada node 'text' yang array dan berisi dialog
                def recursive_check(obj):
                    nonlocal found
                    if isinstance(obj, dict):
                        for k, v in obj.items():
                            if k == "text" and isinstance(v, list):
                                if any(is_dialog_rpgm(line) for line in v):
                                    found = True
                                    return
                            recursive_check(v)
                    elif isinstance(obj, list):
                        for item in obj:
                            recursive_check(item)
                recursive_check(data)
                if found:
                    dialog_files.append(fname)
            except Exception as e:
                continue
        return dialog_files

# ---- Cara pakai ----
# Ganti 'Game.zip' dengan path ZIP game kamu
if __name__ == "__main__":
    zipname = "Game.zip"
    hasil = scan_zip_for_dialogs(zipname)
    print("File yang mengandung dialog RPGM:")
    for f in hasil:
        print(f)