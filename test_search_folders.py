from menu import search_folders
from unittest.mock import patch

def test_search_folders():
    # Test case 1: Valid folder name, confirm with 'y', add more with 'y'
    with patch('builtins.input', side_effect=["ValidFolder", "y", "y"]):
        folders = []
        search_folders()

    assert folders == ["ValidFolder"]

    # Test case 2: Invalid folder name, confirm with 'n'
    with patch('builtins.input', side_effect=["Invalid123", "n"]):
        folders = []
        search_folders()

    assert folders == []

    # Test case 3: Valid folder name, confirm with invalid input, add more with 'n'
    with patch('builtins.input', side_effect=["FolderWithSpaces", "invalid", "n"]):
        folders = []
        search_folders()

    assert folders == ["FolderWithSpaces"]

    print("All test cases passed for search_folders function!")

if __name__ == "__main__":
    test_search_folders()