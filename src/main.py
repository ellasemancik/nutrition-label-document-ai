from ocr_reader import read_text
from preprocess import make_thresholded


original_image = "data/raw/label_02/label_02_per_serving_only.png"

threshold_values = [100, 140, 180]

for threshold in threshold_values:
    image_output = (
        f"data/outputs/label_02/"
        f"label_02_threshold_{threshold}.png"
    )

    text_output = (
        f"data/outputs/label_02/"
        f"label_02_threshold_{threshold}_ocr.txt"
    )

    make_thresholded(
        original_image,
        image_output,
        threshold
    )

    text = read_text(image_output)

    with open(text_output, "w", encoding="utf-8") as file:
        file.write(text)

    print(f"\nThreshold {threshold}:")
    print(text)