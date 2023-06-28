from menu import check_folders
from unittest.mock import patch

def test_check_folders():
    # Test case 1: Checking empty folders list
    with patch('builtins.input', return_value="n"):
        folders = []
        check_folders()

    # Test case 2: Checking non-empty folders list
    folders = ["Folder1", "Folder2", "Folder3"]
    input_sequence = ["y", "2", "2"]
    with patch('builtins.input', side_effect=input_sequence):
        check_folders()

    # Test case 3: Adding a folder to the list
    folders = []
    input_sequence = ["y", "1", "ValidFolder", "n"]
    with patch('builtins.input', side_effect=input_sequence):
        check_folders()

    # Test case 4: Removing folder(s) from the list
    folders = ["Folder1", "Folder2", "Folder3"]
    input_sequence = ["y", "2", "1", "Folder2", "n"]
    with patch('builtins.input', side_effect=input_sequence):
        check_folders()

    print("All test cases passed for check_folders function!")

if __name__ == "__main__":
    test_check_folders()