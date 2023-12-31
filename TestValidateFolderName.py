
# Generated by CodiumAI
from face_crop import validate_folder_name


import unittest

class TestValidateFolderName(unittest.TestCase):

    # Tests that the function validates a folder name of length 1
    def test_valid_folder_name_length_1(self):
        with self.assertRaises(ValueError):
            validate_folder_name("")

    # Tests that the function validates a folder name of length 255
    def test_valid_folder_name_length_255(self):
        folder_name = "a" * 255
        self.assertIsNone(validate_folder_name(folder_name))

    # Tests that the function validates a folder name of length between 1 and 255
    def test_valid_folder_name_length_between_1_and_255(self):
        folder_name = "a" * 100
        self.assertIsNone(validate_folder_name(folder_name))

    # Tests that the function raises a ValueError for an empty folder name
    def test_invalid_empty_folder_name(self):
        with self.assertRaises(ValueError):
            validate_folder_name("")

    # Tests that the function raises a ValueError for a folder name of length 256
    def test_invalid_folder_name_length_256(self):
        folder_name = "a" * 256
        with self.assertRaises(ValueError):
            validate_folder_name(folder_name)

    # Tests that the function raises a ValueError for a folder name containing special characters
    def test_invalid_folder_name_with_special_characters(self):
        folder_name = "folder!"
        with self.assertRaises(ValueError):
            validate_folder_name(folder_name)