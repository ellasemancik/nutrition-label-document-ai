from ocr_reader import read_text


text = read_text("data/raw/label_01.png")

print("OCR result:")
print(text)