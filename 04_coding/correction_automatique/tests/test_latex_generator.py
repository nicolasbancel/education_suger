import unittest
from src.utils.latex_generator import create_latex_document

class TestLatexGenerator(unittest.TestCase):

    def test_create_latex_document(self):
        # Test data
        image_path = "data/output/exercise.png"
        correction_text = "This is the correction for the exercise."

        # Call the function to test
        result = create_latex_document(image_path, correction_text)

        # Check if the result is a valid LaTeX document structure
        self.assertIn("\\documentclass{article}", result)
        self.assertIn("\\begin{document}", result)
        self.assertIn("\\includegraphics{data/output/exercise.png}", result)
        self.assertIn(correction_text, result)
        self.assertIn("\\end{document}", result)

if __name__ == '__main__':
    unittest.main()