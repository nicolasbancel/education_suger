import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os

BUFFER = 10  # pixels to add to the crop area
IMAGE_PATH = (
    "/Users/nicolasbancel/git/education_suger/09_coding/data/exemple_image_pc_1ere.jpg"
)
# PIXEL_COORDS = [[1363, 960], [1363, 1232]]
COLUMNS = [487, 508, 484, 569]
PIXEL_COORDS = [[1605, 1063], [1605, 1278]]


def split_columns(image_path, columns, output_dir="cropped_columns"):
    image = Image.open(image_path)
    width, height = image.size

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    start_x = 0
    for i, col_width in enumerate(columns):
        end_x = start_x + col_width
        cropped = image.crop((start_x, 0, end_x, height))
        output_path = os.path.join(output_dir, f"colonne_{i + 1}.png")
        cropped.save(output_path)
        print(f"Colonne {i + 1} sauvegardée : {output_path}")
        start_x = end_x


# Exemple d'utilisation :
COLUMNS = [487, 508, 484, 569]
crop_columns("exemple_image_pc_1ere.jpg", COLUMNS)


def annotate_pixels(
    image_path,
    pixel_coords=None,
    boxes_coords=None,
    output_path="annotated_image.png",
    color="red",
    radius=5,
    font_size=40,
):
    """
    Annote l'image avec :
    - des cercles sur des pixels (avec texte) si pixel_coords est fourni
    - des rectangles autour de bounding boxes si boxes_coords est fourni
    """
    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", size=font_size)
    except IOError:
        font = ImageFont.load_default()

    # Annotations pour les points individuels
    if pixel_coords:
        for i, (x, y) in enumerate(pixel_coords):
            draw.ellipse(
                [(x - radius, y - radius), (x + radius, y + radius)],
                fill=color,
                outline=color,
            )
            label = f"{i+1}er exercice : x={x} y={y}"
            draw.text((x + radius + 5, y - radius), label, fill=color, font=font)

    # Annotations pour les boîtes (bounding boxes)
    if boxes_coords:
        for i, box in enumerate(boxes_coords):
            top_left = box["bounding_box"]["top_left"]
            bottom_right = box["bounding_box"]["bottom_right"]
            draw.rectangle(
                [tuple(top_left), tuple(bottom_right)], outline=color, width=3
            )
            label = f"Ex {box['exercice']}"
            draw.text(
                (top_left[0] + 5, top_left[1] - font_size), label, fill=color, font=font
            )

    image.save(output_path)
    print(f"Image annotée sauvegardée dans : {output_path}")


def cropped_coordinates(columns, exercise_boundaries):
    image_width = sum(columns)
    average_column_width = image_width / len(columns)

    # columns = [596, 459, 491, 502]
    # exercise_boundaries = [[1363, 960], [1363, 1232]]
    pixel_start = [0]
    for width in columns[:-1]:
        pixel_start.append(pixel_start[-1] + width)

    # Le début de l'exercice peut être avant le début de la colonne
    # Ce qui importe c'est l'ensemble de l'exercice
    exercice_x = exercise_boundaries[0][0] + average_column_width / 2

    for i in range(len(pixel_start) - 1):
        if pixel_start[i] <= exercice_x < pixel_start[i + 1]:
            exercice_column = i
            break
    else:
        exercice_column = len(pixel_start) - 1  # dernière colonne si rien trouvé

    x1 = exercise_boundaries[0][0] - BUFFER
    y1 = exercise_boundaries[0][1] - BUFFER
    # Method #1 for x2 : using the average column width
    x2 = (
        image_width
        if exercice_column == len(columns) - 1
        else x1 + average_column_width + BUFFER
    )
    # Before the beginning of the next exercice
    y2 = exercise_boundaries[1][1] - BUFFER

    top_left = (x1, y1)
    bottom_right = (x2, y2)

    return top_left, bottom_right, exercice_column


def crop_base64_image(image_path, top_left, bottom_right, cropped_image_name):
    """
    Crop a base64 image using the provided coordinates.

    :param image_path: Path to the image file.
    :param top_left: Tuple of (x, y) coordinates for the top-left corner.
    :param bottom_right: Tuple of (x, y) coordinates for the bottom-right corner.
    :return: Base64 encoded string of the cropped image.
    """
    # 1. Open the image from file
    with Image.open(image_path) as image:
        print("Image size:", image.size)
        width, height = image.size
        # 2. Crop the image using the coordinates
        x1, y1 = top_left
        x2, y2 = bottom_right

        cropped = image.crop((x1, y1, x2, y2))  # (left, upper, right, lower)

    # 3. Save cropped image to a buffer as PNG
    buffer = BytesIO()
    cropped.save(buffer, format="PNG")
    buffer.seek(0)

    # 4. Encode back to base64
    cropped_base64 = base64.b64encode(buffer.read()).decode("utf-8")

    # Optional: write to file for verification
    with open(cropped_image_name, "wb") as f:
        f.write(base64.b64decode(cropped_base64))
    # return cropped_base64


def crop_base64_image_old(image_path, top_left, bottom_right):
    # 1. Open the image from file
    with Image.open(image_path) as image:
        print("Image size:", image.size)
        width, height = image.size
        # 2. Crop the image using the coordinates
        x1, y1 = top_left
        print("Top left coordinates:", x1, y1)
        x2, y2 = bottom_right
        print("Bottom right coordinates:", x2, y2)

        if x2 > image.width or y2 > image.height:
            print("⚠️ Coordinates exceed image bounds!")

        x1 = max(0, min(x1, width))
        y1 = max(0, min(y1, height))
        x2 = max(0, min(x2, width))
        y2 = max(0, min(y2, height))

        # Ensure top-left < bottom-right
        if x1 >= x2 or y1 >= y2:
            raise ValueError(f"Invalid crop coordinates: ({x1}, {y1}) to ({x2}, {y2})")

        print(f"Cropping area: ({x1}, {y1}) -> ({x2}, {y2})")

        # x1, x2 = sorted([max(0, min(x1, width)), max(0, min(x2, width))])
        # y1, y2 = sorted([max(0, min(y1, height)), max(0, min(y2, height))])

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


def crop_base64_image_next_exercice(image_path, current_exo, next_exo, width_exo):
    # 1. Open the image from file
    with Image.open(image_path) as image:
        print("Image size:", image.size)
        width, height = image.size

        x1, y1 = current_exo
        x2 = x1 + width_exo
        y2 = next_exo[1]

        print("Top left coordinates:", x1, y1)
        print("Bottom right coordinates:", x2, y2)

        if x2 > width or y2 > height:
            print("⚠️ Coordinates exceed image bounds!")

        x1 = max(0, min(x1, width))
        y1 = max(0, min(y1, height))
        x2 = max(0, min(x2, width))
        y2 = max(0, min(y2, height))

        if x1 >= x2 or y1 >= y2:
            raise ValueError(f"Invalid crop coordinates: ({x1}, {y1}) to ({x2}, {y2})")

        print(f"Cropping area: ({x1}, {y1}) -> ({x2}, {y2})")
        cropped = image.crop((x1, y1, x2, y2))  # (left, upper, right, lower)

    # 2. Save cropped image to buffer
    buffer = BytesIO()
    cropped.save(buffer, format="PNG")
    buffer.seek(0)

    # 3. Encode to base64
    cropped_base64 = base64.b64encode(buffer.read()).decode("utf-8")

    # 4. Optional: write to file for verification
    with open("cropped_output_exercices_limites.png", "wb") as f:
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

    ##################### IPYTHON ###########################
    BUFFER = 10  # pixels to add to the crop area
    IMAGE_PATH = "/Users/nicolasbancel/git/education_suger/09_coding/data/exemple_image_pc_1ere.jpg"
    # PIXEL_COORDS = [[1363, 960], [1363, 1232]]
    COLUMNS = [487, 508, 484, 569]
    PIXEL_COORDS = [[1605, 1063], [1605, 1278]]

    annotate_pixels(
        IMAGE_PATH,
        PIXEL_COORDS,
        output_path="annotated_image_2.png",
        color="red",
        radius=5,
        font_size=40,
    )

    # poetry run python image_processing.py
    # IImage size: (2048, 1470)

    image_path = "/Users/nicolasbancel/git/education_suger/09_coding/data/exemple_image_pc_1ere.jpg"

    # OLD coordinates = {"top_left": [551, 1675], "bottom_right": [1025, 1998]}

    # After correction and providing the dimensions of the image
    # coordinates = {"top_left": [1140, 600], "bottom_right": [1560, 920]}

    # Après expliquer que les exercices se suivent et qu'il faut isoler l'encadré
    # coordinates = {"top_left": [1035, 748], "bottom_right": [1605, 1045]}

    # Liste réponses
    # coordinates = {"top_left": [551, 1675], "bottom_right": [1025, 1998]}
    # coordinates = {"top_left": [1140, 600], "bottom_right": [1560, 920]}
    # coordinates = {"top_left": [1035, 748], "bottom_right": [1605, 1045]}

    # Données par le chat (UI) de ChatGPT
    # Faux : coordinates = {"top_left": [1102, 38], "bottom_right": [2048, 1468]}
    # Faux mais presque : coordinates = {"top_left": [1460, 490], "bottom_right": [2000, 790]}
    coordinates = {"top_left": [1410, 470], "bottom_right": [2000, 930]}

    # image_path = "/mnt/data/exemple_image_pc_1ere.jpg"
    current_exo = [1459, 471]  # Exo 20
    next_exo = [1455, 950]  # Exo 21
    width_exo = 352

    top_left = coordinates["top_left"]
    bottom_right = coordinates["bottom_right"]

    crop_base64_image(image_path, top_left, bottom_right)

    crop_base64_image_next_exercice(
        image_path,
        current_exo=[1459, 471],
        next_exo=[1455, 950],
        width_exo=352,
    )
