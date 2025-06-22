import os
import shutil
from datetime import date
from pathlib import Path
import json

source_dir = '.'

destination_dir = 'build'

extensions = ['.json', '.png', '.mcmeta', '.glsl', '.vsh', '.fsh', '.ogg']

def add(file: str, *lines: str):
    dst_file = f"build/{os.path.split(file)[0]}"
    try:
        os.makedirs(dst_file)
    except:
        None
    shutil.copy2(file, dst_file)
    if len(lines) == 0: return
    with open(f"build/{file}", 'a') as f:
        f.writelines(lines)

def model():
    try:
        os.makedirs("build/assets/minecraft/items")
    except: None
    p = Path("build/assets/minecraft/models/item/")
    for x in p.rglob("*"):
        if f"{x}".endswith(".json"):
            name = f"{x}"[:-5]
            new_data = {
              "model": {
                "type": "range_dispatch",
                "property": "custom_model_data",
                "entries": [],
                "fallback": {
                  "type": "model",
                  "model": f"item/{os.path.basename(f"{x}")[:-5]}"
                }
              }
            }
            data = {}
            with open(f"{x}", "r") as file:
                data = json.load(file)
                file.close()
            if not("overrides" in data.keys()):
                print(name, "x")
                continue
            overrides = data["overrides"]
            for predicate in overrides:
                if "custom_model_data" in predicate["predicate"].keys():
                    entry = {
                        "threshold": predicate["predicate"]["custom_model_data"],
                        "model": {
                          "type": "model",
                          "model": predicate["model"]
                        }
                    }
                    new_data["model"]["entries"].append(entry)
            with open(f"build/assets/minecraft/items/{os.path.basename(f"{x}")}", "w") as file:
                json.dump(new_data, file, indent=2)
                file.close()
            print(name, "o")


for filename in os.listdir(destination_dir):
    file_path = os.path.join(destination_dir, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

for root, dirs, files in os.walk(source_dir):
    rel_path = os.path.relpath(root, source_dir)
    if rel_path.startswith(".git") or rel_path.startswith("build"): continue
    target_root = os.path.join(destination_dir, rel_path)
    os.makedirs(target_root, exist_ok=True)
    
    for file in files:
        if any(file.lower().endswith(ext) for ext in extensions):
            src_file = os.path.join(root, file)
            dst_file = os.path.join(target_root, file)
            shutil.copy2(src_file, dst_file)
    print(rel_path)
print(f'-- UPDATE')
model()
print(f'-- CREATE LICENSE')
add("license.txt")
today = date.today()
mounths = [ "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec" ]
add("readme.txt", f"\nBuild: {today.day} {mounths[today.month - 1]} {today.year}")
print(f'-- ZIP')
archiveName = f"shiver2_{today.day}_{today.month}_{today.year}"
shutil.make_archive(archiveName, 'zip', 'build')
shutil.move(f"{archiveName}.zip", "build")
print(f'----> BUILDED <----')