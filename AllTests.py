import unittest
from TestChooseOption import TestChooseOption
from TestCropFaces import TestCropFaces
from TestInputValidation import TestInputValidation
from TestListFolders import TestListFolders
from TestMain import TestMain
from TestPauseForSeconds import TestPauseForSeconds
from TestPrintFolders import TestPrintFolders
from TestRemoveFolders import TestRemoveFolders
from TestRetrieveFolderFromWindows import TestRetrieveFolderFromWindows
from TestSearchFolders import TestSearchFolders
from TestValidateFolderName import TestValidateFolderName
from TestValidateInput import TestValidateInput


if __name__ == '__main__':
    loader = unittest.TestLoader()

    # Create a test suite
    suite = unittest.TestSuite()

    # Add tests to the suite in the desired order
    test_classes = [
        TestChooseOption, TestCropFaces, TestInputValidation,
        TestListFolders, TestMain, TestPauseForSeconds,
        TestPrintFolders, TestRemoveFolders, TestRetrieveFolderFromWindows,
        TestSearchFolders, TestValidateFolderName, TestValidateInput
    ]
    for test_class in test_classes:
        suite.addTest(loader.loadTestsFromTestCase(test_class))

    # Run the tests
    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    # Check if any failures occurred
    if len(result.failures) > 0:
        print(f"\nNumber of failures: {len(result.failures)}")
    else:
        print("\nAll tests passed.")