
from pathlib import Path

from preprocess import make_grayscale, make_larger, make_thresholded
from ocr_reader import read_text

# Test on label 07 first
image_path = Path("data/raw/label_08/label_08.png")
output_dir = Path("data/outputs/ocr_tests_label_08")
output_dir.mkdir(parents=True, exist_ok=True)

# Create different versions of the same image
gray_path = output_dir / "label_07_gray.png"
large_path = output_dir / "label_07_large.png"
threshold_path = output_dir / "label_07_threshold.png"

make_grayscale(image_path, gray_path)
make_larger(image_path, large_path)
make_thresholded(image_path, threshold_path)

# Try different image versions and OCR settings
tests = [
    ("original_psm6", image_path, "--psm 6"),
    ("original_psm11", image_path, "--psm 11"),
    ("grayscale_psm6", gray_path, "--psm 6"),
    ("large_psm6", large_path, "--psm 6"),
    ("large_psm11", large_path, "--psm 11"),
    ("threshold_psm6", threshold_path, "--psm 6"),
    ("threshold_psm11", threshold_path, "--psm 11"),
]

for name, path, config in tests:
    text = read_text(path, config=config)

    # Save each OCR result so we can compare them
    result_path = output_dir / f"{name}.txt"
    result_path.write_text(text, encoding="utf-8")

    print(f"\n{name}")
    print("-" * 40)
    print(text[:500])

print("\nAll OCR tests completed.")
