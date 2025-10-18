import unittest

from exceptions import VMTranslatorError
from utils import is_valid_vm_file

class TestUtils(unittest.TestCase):

    def test_is_valid_vm_file_success(self):
        """Correct result with valid input"""
        result = is_valid_vm_file('test.vm')
        self.assertIsNone(result)

    def test_is_valid_vm_file_missing_extension(self):
        """Missing file extension"""
        with self.assertRaises(VMTranslatorError):
            is_valid_vm_file('test')

    def test_is_valid_vm_file_wrong_extension(self):
        """Incorrect file extension"""
        with self.assertRaises(VMTranslatorError):
            is_valid_vm_file('test.asm')
