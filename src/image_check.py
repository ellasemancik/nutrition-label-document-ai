from PIL import Image


def check_image(image_path):
    try:
        image = Image.open(image_path)

        image_info = {
            "width": image.width,
            "height": image.height,
            "format": image.format
        }

        print("Image opened successfully")
        print("Width:", image.width)
        print("Height:", image.height)
        print("Format:", image.format)

        return image_info

    except FileNotFoundError:
        print("The image could not be found.")
        return None

    except Exception as error:
        print("Something went wrong:", error)
        return None