from PIL import Image


def make_grayscale(image_path, output_path):
    image = Image.open(image_path)

    grayscale_image = image.convert("L")

    grayscale_image.save(output_path)

    return output_path