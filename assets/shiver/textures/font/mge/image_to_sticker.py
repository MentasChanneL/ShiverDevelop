import sys
import os
from PIL import Image

def convert_to_png_resize(input_path):
    """Конвертирует изображение в PNG и сжимает до 256x256"""
    
    # Проверяем существование файла
    if not os.path.exists(input_path):
        print(f"Файл не найден: {input_path}")
        return
    
    # Формируем выходной путь (меняем расширение на .png)
    base_name = os.path.splitext(input_path)[0]
    output_path = f"{base_name}.png"
    
    try:
        # Открываем изображение
        with Image.open(input_path) as img:
            # Конвертируем в RGBA (для поддержки прозрачности)
            if img.mode not in ('RGBA', 'RGB', 'P'):
                img = img.convert('RGBA')
            
            # Изменяем размер до 256x256
            img_resized = img.resize((256, 256), Image.Resampling.LANCZOS)
            
            # Сохраняем как PNG
            img_resized.save(output_path, 'PNG', optimize=True)
            
            print(f"✅ Готово! Файл сохранён: {output_path}")
            print(f"   Размер: {img_resized.size[0]}x{img_resized.size[1]}")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Перетащите изображение на этот скрипт")
        input("Нажмите Enter для выхода...")
    else:
        for file_path in sys.argv[1:]:
            convert_to_png_resize(file_path)