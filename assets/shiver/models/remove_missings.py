import json
import sys
from pathlib import Path

def clean_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if 'elements' in data:
        for element in data['elements']:
            if 'faces' in element:
                # Удаляем все faces с texture "#missing"
                element['faces'] = {k: v for k, v in element['faces'].items() 
                                   if v.get('texture') != '#missing'}
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent='\t', ensure_ascii=False)

if __name__ == "__main__":
    folder = Path(sys.argv[1] if len(sys.argv) > 1 else '.')
    for json_file in folder.rglob('*.json'):
        clean_json(json_file)
        print(f"Обработан: {json_file}")