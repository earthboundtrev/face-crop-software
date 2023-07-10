import unittest
from unittest import mock
from menu import crop_image_selector

def crop_faces():
    """Stub function for cropping faces"""
    pass

def crop_eyes():
    """Stub function for cropping eyes"""
    pass

def crop_eyes_noses():
    """Stub function for cropping eyes and noses"""
    pass

def pause_screen(seconds):
    """Stub function for pausing the screen"""
    pass

def input_validation(prompt, func=None):
    """Validate user input based on provided function"""
    while True:
        user_input = input(prompt)
        if func is not None and not func(user_input):
            print("Invalid input. Please try again.")
            user_input = None
        return user_input

class TestCropImageSelector(unittest.TestCase):
    def test_crop_image_selector_faces(self):
        # Test cropping faces
        with mock.patch('builtins.input', return_value='1'):
            with mock.patch('builtins.print') as mock_print:
                crop_image_selector()
                mock_print.assert_called_with("Returning to the main menu...")

    def test_crop_image_selector_eyes(self):
        # Test cropping eyes
        with mock.patch('builtins.input', return_value='2'):
            with mock.patch('builtins.print') as mock_print:
                crop_image_selector()
                mock_print.assert_called_with("Returning to the main menu...")

    def test_crop_image_selector_eyes_noses(self):
        # Test cropping eyes and noses
        with mock.patch('builtins.input', return_value='3'):
            with mock.patch('builtins.print') as mock_print:
                crop_image_selector()
                mock_print.assert_called_with("Returning to the main menu...")

    def test_crop_image_selector_invalid_input(self):
        # Test invalid input
        with mock.patch('builtins.input', return_value='invalid'):
            with mock.patch('builtins.print') as mock_print:
                with mock.patch('time.sleep'):
                    crop_image_selector()
                    mock_print.assert_called_with("Invalid choice. Please select a number between 1 and 4.")

class TestInputValidation(unittest.TestCase):
    def test_input_validation_valid_input(self):
        # Test valid input
        with mock.patch('builtins.input', return_value='2'):
            user_input = input_validation("Enter your choice: ", lambda x: x.isdigit() and 1 <= int(x) <= 4)
            self.assertEqual(user_input, '2')

    def test_input_validation_invalid_input(self):
        # Test invalid input
        with mock.patch('builtins.input', return_value='abc'):
            with mock.patch('builtins.print') as mock_print:
                with mock.patch('time.sleep'):
                    user_input = input_validation("Enter your choice: ", lambda x: x.isdigit() and 1 <= int(x) <= 4)
                    self.assertIsNone(user_input)
                    mock_print.assert_called_with("Invalid input. Please try again.")

if __name__ == '__main__':
    unittest.main()