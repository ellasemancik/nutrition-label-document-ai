from PIL import Image


def make_grayscale(image_path, output_path):
    image = Image.open(image_path)
    grayscale_image = image.convert("L")
    grayscale_image.save(output_path)

    return output_path


def make_larger(image_path, output_path):
    image = Image.open(image_path)

    new_width = image.width * 2
    new_height = image.height * 2

    larger_image = image.resize((new_width, new_height))
    larger_image.save(output_path)

    return output_path