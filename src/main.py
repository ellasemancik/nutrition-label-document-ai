from ocr_reader import read_text


image_path = "data/raw/label_01.png"
output_path = "data/outputs/label_01_ocr.txt"

text = read_text(image_path)

print("OCR result:")
print(text)

with open(output_path, "w", encoding="utf-8") as output_file:
    output_file.write(text)

print("OCR result saved to:", output_path)