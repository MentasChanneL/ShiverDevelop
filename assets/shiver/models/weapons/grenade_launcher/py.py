import json
from pathlib import Path

for json_file in Path(".").rglob("*.json"):
    data = json.loads(json_file.read_text(encoding="utf-8"))
    if "display" in data and "firstperson_lefthand" in data["display"]:
        del data["display"]["firstperson_lefthand"]
        json_file.write_text(json.dumps(data, indent="\t", ensure_ascii=False), encoding="utf-8")
        print(json_file)