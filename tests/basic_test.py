import sys
sys.path.append('..')

import csvfilter
import unittest

# Define a test suite targeting specific functionality
class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""
    def test_that_main_module_function_is_solved(self):
        solved = csvfilter.main_module_function()
        self.assertTrue(solved)


if __name__ == '__main__':
    unittest.main()