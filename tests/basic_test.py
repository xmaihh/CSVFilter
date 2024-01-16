import sys
import os

sys.path.append("../csvfilter")
current_path = os.getcwd()

print("Current path:", current_path)

import csv_toolbox
import unittest


# Define a test suite targeting specific functionality
class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_that_main_module_function_is_solved(self):
        solved = csv_toolbox.main_module_function()
        self.assertTrue(solved)


if __name__ == "__main__":
    unittest.main()
