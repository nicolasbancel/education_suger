import base64
from io import BytesIO
from PIL import Image


def crop_base64_image(image_path, top_left, bottom_right):
    # 1. Open the image from file
    with Image.open(image_path) as image:
        print("Image size:", image.size)
        # 2. Crop the image using the coordinates
        x1, y1 = top_left
        x2, y2 = bottom_right
        if x2 > image.width or y2 > image.height:
            print("⚠️ Coordinates exceed image bounds!")

        cropped = image.crop((x1, y1, x2, y2))  # (left, upper, right, lower)

    # image_data = base64.b64decode(base64_str)
    # image = Image.open(BytesIO(image_data))

    # 3. Save cropped image to a buffer as PNG
    buffer = BytesIO()
    cropped.save(buffer, format="PNG")
    buffer.seek(0)

    # 4. Encode back to base64
    cropped_base64 = base64.b64encode(buffer.read()).decode("utf-8")

    # Optional: write to file for verification
    with open("cropped_output.png", "wb") as f:
        f.write(base64.b64decode(cropped_base64))
    return cropped_base64


def load_image(image_path):
    from PIL import Image

    return Image.open(image_path)


def crop_image(image, crop_area):
    return image.crop(crop_area)


def save_image(image, output_path):
    image.save(output_path)


if __name__ == "__main__":
    image_path = "/Users/nicolasbancel/git/education_suger/09_coding/data/exemple_image_pc_1ere.jpg"
    coordinates = {"top_left": [551, 1675], "bottom_right": [1025, 1998]}
    top_left = coordinates["top_left"]
    bottom_right = coordinates["bottom_right"]

    crop_base64_image(image_path, top_left, bottom_right)
