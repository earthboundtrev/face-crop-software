import unittest

from io import StringIO
from unittest.mock import patch

from menu import validate_folder_name, input_validation, main, choose_option, search_folders, check_folders


class TestFolderNameValidation(unittest.TestCase):
    def test_valid_folder_name(self):
        self.assertEqual(validate_folder_name("folder"), "folder")

    def test_invalid_folder_name_with_spaces(self):
        with self.assertRaises(ValueError):
            validate_folder_name("invalid name")

    def test_invalid_folder_name_with_numbers(self):
        with self.assertRaises(ValueError):
            validate_folder_name("folder1")


class TestInputValidation(unittest.TestCase):
    def setUp(self):
        self.mock_input = "test"

    @patch("builtins.input", return_value=self.mock_input)
    def test_valid_input(self, mock_input):
        result = input_validation("Enter some text: ")
        self.assertEqual(result, self.mock_input)

    @patch("builtins.input", side_effect=["", "test"])
    def test_empty_input_and_then_valid_input(self, mock_input):
        with patch("sys.stdout", new=StringIO()) as fake_stdout:
            result = input_validation("Enter some text: ")
            self.assertEqual(fake_stdout.getvalue().strip(), "Invalid input. Please try again.")
            self.assertEqual(result, self.mock_input)

    @patch("builtins.input", return_value="invalid")
    def test_invalid_input(self, mock_input):
        with patch("sys.stdout", new=StringIO()) as fake_stdout:
            result = input_validation("Enter some text: ", lambda x: x.isnumeric())
            self.assertEqual(fake_stdout.getvalue().strip(), "Invalid input. Please try again.")
            self.assertIsNone(result)


class TestChooseOption(unittest.TestCase):
    @patch("builtins.input", return_value="1")
    def test_valid_input(self, mock_input):
        with patch("sys.stdout", new=StringIO()):
            result = choose_option()
            self.assertEqual(result, 1)

    @patch("builtins.input", side_effect=["invalid", "2"])
    def test_invalid_input_and_then_valid_input(self, mock_input):
        with patch("sys.stdout", new=StringIO()) as fake_stdout:
            result = choose_option()
            self.assertEqual(fake_stdout.getvalue().strip(), "Invalid input. Please try again.")
            self.assertEqual(result, 2)

    @patch("builtins.input", side_effect=["5", "3", "1"])
    def test_input_out_of_range_and_then_valid_input(self, mock_input):
        with patch("sys.stdout", new=StringIO()):
            result = choose_option()
            self.assertEqual(result, 1)


class TestMain(unittest.TestCase):
    @patch("builtins.input", side_effect=["1", "4"])
    def test_main_menu(self, mock_input):
        with patch("sys.stdout"):
            main()


class TestSearchFolders(unittest.TestCase):
    def setUp(self):
        self.mock_folder_name = "valid_folder"

    @patch("builtins.input", side_effect=["invalid name", self.mock_folder_name, "invalid answer", "y", "invalid answer", "n"])
    def test_invalid_input_and_then_valid_input(self, mock_input):
        with patch("sys.stdout", new=StringIO()) as fake_stdout:
            search_folders()
            expected_output = [
                "What folder did you want to search for?",
                "Invalid input. Please try again.",
                "Folder name:",
                "Validated folder name: valid_folder",
                "Confirm? (y/n): ",
                "Invalid input. Please try again.",
                "Confirm? (y/n): ",
                "This is the full list of folders ['valid_folder']",
                "Add more folders? (y/n): ",
                "Invalid input. Please try again.",
                "Add more folders? (y/n): ",
            ]
            output = [line.strip() for line in fake_stdout.getvalue().split("\n")]
            self.assertListEqual(output, expected_output)


class TestCheckFolders(unittest.TestCase):
    @patch("menu.check_folders", return_value=["folder1", "folder2"])
    @patch("builtins.input", return_value="y")
    def test_check_folders_yes(self, mock_input, mock_check_folders):
        with patch("sys.stdout", new=StringIO()) as fake_stdout:
            result = check_folders()
            self.assertEqual(fake_stdout.getvalue().strip(), "This is the full list of folders ['folder1', 'folder2']")
            self.assertEqual(mock_check_folders.call_count, 1)
            self.assertEqual(result, ["folder1", "folder2"])

    @patch("menu.check_folders", return_value=["folder1", "folder2"])
    @patch("builtins.input", return_value="n")
    def test_check_folders_no(self, mock_input, mock_check_folders):
        with patch("sys.stdout") as fake_stdout:
            result = check_folders()
            self.assertEqual(fake_stdout.getvalue().strip(), "")
            self.assertEqual(mock_check_folders.call_count, 1)
            self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()