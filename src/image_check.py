from PIL import Image


def check_image(image_path):
    try:
        image = Image.open(image_path)

        print("Image opened successfully")
        print("Width:", image.width)
        print("Height:", image.height)
        print("Format:", image.format)

    except FileNotFoundError:
        print("The image could not be found.")

    except Exception as error:
        print("Something went wrong:", error)