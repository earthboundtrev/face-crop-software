from menu import validate_folder_name

def test_validate_folder_name():
    # Test case 1: Valid folder name
    folder_name = "ValidFolder"
    result = validate_folder_name(folder_name)
    assert result == folder_name

    # Test case 2: Folder name with leading/trailing spaces
    folder_name = "  FolderWithSpaces  "
    expected_result = "FolderWithSpaces"
    result = validate_folder_name(folder_name)
    assert result == expected_result

    # Test case 3: Invalid folder name with numbers
    folder_name = "Folder123"
    try:
        validate_folder_name(folder_name)
    except ValueError:
        pass
    else:
        assert False, "Expected ValueError for invalid folder name"

    print("All test cases passed for validate_folder_name function!")

if __name__ == "__main__":
    test_validate_folder_name()