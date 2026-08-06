from ocr_reader import read_text
from preprocess import make_grayscale


original_image = "data/raw/label_01.png"
grayscale_image = "data/outputs/label_01_grayscale.png"

original_output = "data/outputs/label_01_original_ocr.txt"
grayscale_output = "data/outputs/label_01_grayscale_ocr.txt"

make_grayscale(original_image, grayscale_image)

original_text = read_text(original_image)
grayscale_text = read_text(grayscale_image)

with open(original_output, "w", encoding="utf-8") as file:
    file.write(original_text)

with open(grayscale_output, "w", encoding="utf-8") as file:
    file.write(grayscale_text)

print("Finished comparing original and grayscale OCR.")