import unittest
from src.utils.image_processing import load_image, crop_exercise, save_cropped_image

class TestImageProcessing(unittest.TestCase):

    def setUp(self):
        self.image_path = 'data/input/sample_image.png'
        self.cropped_image_path = 'data/output/cropped_exercise.png'
        self.crop_area = (100, 100, 400, 400)  # Example crop area (left, upper, right, lower)

    def test_load_image(self):
        image = load_image(self.image_path)
        self.assertIsNotNone(image)

    def test_crop_exercise(self):
        image = load_image(self.image_path)
        cropped_image = crop_exercise(image, self.crop_area)
        self.assertIsNotNone(cropped_image)

    def test_save_cropped_image(self):
        image = load_image(self.image_path)
        cropped_image = crop_exercise(image, self.crop_area)
        save_cropped_image(cropped_image, self.cropped_image_path)
        # Check if the cropped image file exists
        self.assertTrue(os.path.exists(self.cropped_image_path))

if __name__ == '__main__':
    unittest.main()