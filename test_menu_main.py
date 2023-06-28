from menu import main
from unittest.mock import patch

def test_main():
    # Test case 1: Choose option 1 (search_folders)
    with patch('builtins.input', return_value="1"):
        with patch('menu.choose_option', return_value=1):
            main()

    # Test case 2: Choose option 2 (check_folders)
    with patch('builtins.input', return_value="2"):
        with patch('menu.choose_option', return_value=2):
            main()

    # Test case 3: Choose option 3 (crop_images)
    with patch('builtins.input', return_value="3"):
        with patch('menu.choose_option', return_value=3):
            main()

    # Test case 4: Choose option 4 (exit)
    with patch('builtins.input', return_value="4"):
        with patch('menu.choose_option', return_value=4):
            main()

    print("All test cases passed for main function!")

if __name__ == "__main__":
    test_main()