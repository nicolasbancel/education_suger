import unittest
from src.utils.correction_logic import correct_exercise

class TestCorrectionLogic(unittest.TestCase):

    def test_correct_exercise_valid(self):
        exercise = "What is 2 + 2?"
        expected_correction = "The answer is 4."
        self.assertEqual(correct_exercise(exercise), expected_correction)

    def test_correct_exercise_invalid(self):
        exercise = "What is 2 + 2?"
        expected_correction = "The answer is 5."
        self.assertNotEqual(correct_exercise(exercise), expected_correction)

    def test_correct_exercise_edge_case(self):
        exercise = "What is 0 + 0?"
        expected_correction = "The answer is 0."
        self.assertEqual(correct_exercise(exercise), expected_correction)

if __name__ == '__main__':
    unittest.main()