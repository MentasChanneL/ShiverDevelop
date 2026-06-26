from PIL import Image
import numpy as np
import os

def process_image(input_path, output_path=None, white_threshold=250):
    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_processed{ext}"

    img = Image.open(input_path).convert('RGB')
    arr = np.array(img, dtype=np.uint8)
    h, w, _ = arr.shape

    for row in range(0, h - 7, 8):
        for col in range(0, w - 7, 8):
            y0, y1 = row, row + 8
            x0, x1 = col, col + 8

            # Находим самый правый столбец с белым пикселем
            max_x = -1
            for dx in range(8):
                column = arr[y0:y1, x0 + dx]
                white_mask = (column[:, 0] > white_threshold) & \
                             (column[:, 1] > white_threshold) & \
                             (column[:, 2] > white_threshold)
                if np.any(white_mask):
                    max_x = dx

            if max_x == -1:
                continue

            # Закрашиваем столбцы от 0 до max_x + 1 (выступ), но не более 7
            right_limit = min(max_x + 2, 8)  # число столбцов
            for dx in range(right_limit):
                for dy in range(8):
                    pixel = arr[y0 + dy, x0 + dx]
                    is_white = (pixel[0] > white_threshold and
                                pixel[1] > white_threshold and
                                pixel[2] > white_threshold)
                    if not is_white:
                        if dy == 7:
                            arr[y0 + dy, x0 + dx] = [85, 67, 67]
                        else:
                            arr[y0 + dy, x0 + dx] = [110, 105, 100]

    result = Image.fromarray(arr)
    result.save(output_path)
    print(f"Сохранено: {output_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 1:
        print("Использование: python script.py input_image.png [output_image.png]")
        sys.exit(1)
    in_file = sys.argv[1]
    out_file = f"er_{sys.argv[1]}"
    process_image(in_file, out_file)