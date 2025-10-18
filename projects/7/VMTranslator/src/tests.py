import unittest

from exceptions import VMTranslatorError
from utils import clean_input_lines, is_valid_vm_file

class TestUtils(unittest.TestCase):

    def test_clean_input_lines(self):
        """."""
        lines = ['\n', '// comment', ' push CONSTANT 1 // inline comment ']
        expected = ['push constant 1 // inline comment']
        output = clean_input_lines(lines)
        self.assertEqual(expected, output)

    def test_is_valid_vm_file_success(self):
        """Correct result with valid input."""
        result = is_valid_vm_file('test.vm')
        self.assertIsNone(result)

    def test_is_valid_vm_file_missing_extension(self):
        """Missing file extension."""
        with self.assertRaises(VMTranslatorError):
            is_valid_vm_file('test')

    def test_is_valid_vm_file_wrong_extension(self):
        """Incorrect file extension."""
        with self.assertRaises(VMTranslatorError):
            is_valid_vm_file('test.asm')
