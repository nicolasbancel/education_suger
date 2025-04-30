# Contents of /auto-correct-tool/auto-correct-tool/src/main.py

import os
from utils.image_processing import load_image, crop_exercise, save_cropped_image
from utils.latex_generator import create_latex_document
from utils.correction_logic import correct_exercise

def main():
    # Load the image of the book page
    input_image_path = os.path.join('data', 'input', 'book_page.png')  # Example input file
    image = load_image(input_image_path)

    # Crop the exercise from the image
    exercise_area = (100, 100, 400, 300)  # Example coordinates (left, top, right, bottom)
    cropped_image = crop_exercise(image, exercise_area)

    # Save the cropped image
    cropped_image_path = os.path.join('data', 'output', 'cropped_exercise.png')
    save_cropped_image(cropped_image, cropped_image_path)

    # Correct the exercise
    correction = correct_exercise(cropped_image)

    # Generate LaTeX document
    latex_output_path = os.path.join('data', 'output', 'exercise_correction.tex')
    create_latex_document(cropped_image_path, correction, latex_output_path)

if __name__ == "__main__":
    main()