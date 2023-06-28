from menu import choose_option
from unittest.mock import patch

def test_choose_option():
    # Test case 1: Valid option (2)
    with patch('builtins.input', return_value="2"):
        result = choose_option()
    assert result == 2

    # Test case 2: Invalid option (5)
    with patch('builtins.input', return_value="5"):
        result = choose_option()
    assert result is None

    # Test case 3: Non-numeric input
    with patch('builtins.input', return_value="abc"):
        result = choose_option()
    assert result is None

    print("All test cases passed for choose_option function!")

if __name__ == "__main__":
    test_choose_option()