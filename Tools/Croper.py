import argparse
import os
from pathlib import Path
import os
from tqdm import tqdm
import cv2

# Вспомогательная функция для нарезки изображений по bbox

if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=True)

    parser.add_argument(
        "--file",
        type=str,
        default="img.png",
        help="Название изображения.",
    )

    parser.add_argument(
        "--dir",
        type=str,
        default="data",
        help="Директория, в которой хранятся изображения.",
    )

    parser.add_argument(
        "--croped_dir",
        type=str,
        default="croped_img",
        help="Директория, в которую будут записаны обрезанные изображения.",
    )

    parser.add_argument(
        "--bbox", 
        default=None, 
        help="Данные по bbox"
        )

    args = parser.parse_args()
    os.makedirs(args.croped_dir, exist_ok=True)

    img = cv2.imread(os.path.join(args.dir, args.file))
    save_path = os.path.join(args.croped_dir, args.file)

    x, y, x_len, y_len =args.bbox

    cropped_image = img[y - (y_len / 2):y + (y_len / 2), x - (x_len / 2):x + (x_len / 2)]

    cv2.imwrite(save_path, cropped_image)