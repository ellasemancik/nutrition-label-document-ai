from PIL import Image

from src.image_check import check_image


def test_check_image_reads_size(tmp_path):
    test_image_path = tmp_path / "test_image.png"

    image = Image.new("RGB", (100, 50))
    image.save(test_image_path)

    result = check_image(test_image_path)

    assert result["width"] == 100
    assert result["height"] == 50
    assert result["format"] == "PNG"