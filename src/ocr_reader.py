from PIL import Image
import pytesseract


def read_text(image_path):
    image = Image.open(image_path)

    text = pytesseract.image_to_string(image)

    return text