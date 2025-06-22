import os
import shutil

source_dir = '.'

destination_dir = 'build'

extensions = ['.json', '.png', '.mcmeta']

for root, dirs, files in os.walk(source_dir):
    rel_path = os.path.relpath(root, source_dir)
    target_root = os.path.join(destination_dir, rel_path)
    os.makedirs(target_root, exist_ok=True)
    
    for file in files:
        if any(file.lower().endswith(ext) for ext in extensions):
            src_file = os.path.join(root, file)
            dst_file = os.path.join(target_root, file)
            shutil.copy2(src_file, dst_file)
            print(src_file)
print(f'----> BUILDED <----')