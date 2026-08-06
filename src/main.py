from ocr_reader import read_text


full_image = "data/raw/label_02/label_02.png"
per_serving_image = "data/raw/label_02/label_02_per_serving_only.png"

full_output = "data/outputs/label_02/label_02_full_ocr.txt"
per_serving_output = "data/outputs/label_02/label_02_per_serving_ocr.txt"


full_text = read_text(full_image)
per_serving_text = read_text(per_serving_image)


with open(full_output, "w", encoding="utf-8") as file:
    file.write(full_text)

with open(per_serving_output, "w", encoding="utf-8") as file:
    file.write(per_serving_text)


print("Full label OCR:")
print(full_text)

print("\nPer-serving OCR:")
print(per_serving_text)