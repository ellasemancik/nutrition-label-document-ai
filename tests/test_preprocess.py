from PIL import Image

from src.preprocess import make_grayscale, make_thresholded

def test_make_grayscale(tmp_path):
    input_path = tmp_path / "input.png"
    output_path = tmp_path / "output.png"

    image = Image.new("RGB", (40, 20))
    image.save(input_path)

    make_grayscale(input_path, output_path)

    result = Image.open(output_path)

    assert result.mode == "L"
    assert result.size == (40, 20)
    
    
def test_make_thresholded(tmp_path):
    input_path = tmp_path / "input.png"
    output_path = tmp_path / "output.png"

    image = Image.new("RGB", (40, 20), "gray")
    image.save(input_path)

    make_thresholded(input_path, output_path)

    result = Image.open(output_path)

    assert result.mode == "L"
    assert result.size == (40, 20)