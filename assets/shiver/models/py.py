import os
import json
import sys
from pathlib import Path

def search_json_files(root_folder):
    """
    Ищет JSON файлы, содержащие "block/" или "missing"
    
    Args:
        root_folder: путь к папке для поиска
    """
    root = Path(root_folder)
    
    if not root.exists():
        print(f"Папка {root_folder} не существует")
        return
    
    # Находим все JSON файлы
    json_files = list(root.rglob("*.json"))
    
    if not json_files:
        print("JSON файлы не найдены")
        return
    
    found_files = []
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Проверяем наличие подстрок
                if "block/" in content or "missing" in content:
                    found_files.append(json_file)
                    print(f"✓ {json_file.relative_to(root)}")
                    
        except Exception as e:
            print(f"✗ Ошибка при чтении {json_file}: {e}")
    
    # Вывод статистики
    print("\n" + "="*50)
    print(f"Всего JSON файлов: {len(json_files)}")
    print(f"Найдено совпадений: {len(found_files)}")
    
    return found_files

def search_json_files_detailed(root_folder):
    """
    Расширенная версия с выводом точных совпадений
    """
    root = Path(root_folder)
    
    if not root.exists():
        print(f"Папка {root_folder} не существует")
        return
    
    json_files = list(root.rglob("*.json"))
    
    if not json_files:
        print("JSON файлы не найдены")
        return
    
    found_files = []
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                matches = []
                if "block/" in content:
                    matches.append("block/")
                if "missing" in content:
                    matches.append("missing")
                
                if matches:
                    found_files.append(json_file)
                    print(f"\n📄 {json_file.relative_to(root)}")
                    print(f"   Найдено: {', '.join(matches)}")
                    
                    # Показываем контекст (опционально)
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if "block/" in line or "missing" in line:
                            print(f"   Строка {i+1}: {line.strip()[:100]}")
                            
        except Exception as e:
            print(f"✗ Ошибка: {json_file} - {e}")
    
    print("\n" + "="*50)
    print(f"Всего JSON файлов: {len(json_files)}")
    print(f"Найдено совпадений: {len(found_files)}")
    
    return found_files

if __name__ == "__main__":
    # Использование
    if len(sys.argv) < 2:
        print("Использование:")
        print("  python script.py /путь/к/папке")
        print("  python script.py /путь/к/папке --detailed  # подробный вывод")
        sys.exit(1)
    
    folder = sys.argv[1]
    detailed = "--detailed" in sys.argv
    
    if detailed:
        search_json_files_detailed(folder)
    else:
        search_json_files(folder)