from menu import input_validation

def test_input_validation():
    # Test case 1: Valid input
    prompt = "Enter a number: "
    valid_input = "123"
    result = input_validation(prompt, lambda x: x.isnumeric())
    assert result == valid_input

    # Test case 2: Invalid input
    prompt = "Enter a name: "
    invalid_input = "123"
    result = input_validation(prompt, lambda x: x.isalpha())
    assert result is None

    # Test case 3: No validation function provided
    prompt = "Enter any text: "
    default_input = "test"
    result = input_validation(prompt)
    assert result == default_input

    print("All test cases passed for input_validation function!")

if __name__ == "__main__":
    test_input_validation()