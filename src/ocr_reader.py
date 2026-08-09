from PIL import Image
import pytesseract


def read_text(image_path, config=""):
    image = Image.open(image_path)

    text = pytesseract.image_to_string(
        image,
        config=config
    )

    return text