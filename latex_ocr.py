import sys
from PIL import Image
from pix2tex import cli as latexocr
import argparse
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  

def recognize_math_expression(image_path: str) -> str:
    """
    Распознает математическое выражение с изображения и возвращает LaTeX-код.

    Параметры:
        image_path (str): Путь к изображению с формулой.
        output_file (str, опционально): Если указан, сохраняет результат в файл.

    Возвращает:
        str: Распознанная формула в LaTeX.
    """
    try:
        model = latexocr.LatexOCR()
        img = Image.open(image_path)
        img = img.convert('L').point(lambda x: 0 if x < 200 else 255, '1')
        latex_formula = model(img)
        print("\n✅ Распознанная формула (LaTeX):")
        print(latex_formula)
        return latex_formula

    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Распознавание математических выражений из изображений.")
    parser.add_argument("image_path", help="image_test.jpg")
    args = parser.parse_args()
    recognize_math_expression(args.image_path)