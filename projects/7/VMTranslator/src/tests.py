import unittest

from exceptions import ParseError, VMTranslatorError
from parser import parse_instruction
from translator import skip_line
from utils import get_vm_file_name

class TestParser(unittest.TestCase):

    def test_parse_instruction_two_parts(self):
        """The instruction has two parts"""
        with self.assertRaises(ParseError):
            parse_instruction(1, 'one two')

class TestTranslator(unittest.TestCase):

    def test_skip_line_no_skip(self):
        """No skip."""
        input = 'push constant 1'.strip().lower()
        output = skip_line(input)
        self.assertFalse(output)

    def test_skip_line_empty(self):
        """Test lines with no content."""
        input = '\n'.strip().lower()
        output = skip_line(input)
        self.assertTrue(output)

    def test_skip_line_comment(self):
        """Test comment line."""
        input = '// comment'.strip().lower()
        output = skip_line(input)
        self.assertTrue(output)

class TestUtils(unittest.TestCase):

    def test_iget_vm_file_name_success(self):
        """Correct result with valid input."""
        result = get_vm_file_name('test.vm')
        self.assertEqual(result, 'test')

    def test_get_vm_file_name_missing_extension(self):
        """Missing file extension."""
        with self.assertRaises(VMTranslatorError):
            get_vm_file_name('test')

    def test_get_vm_file_name_wrong_extension(self):
        """Incorrect file extension."""
        with self.assertRaises(VMTranslatorError):
            get_vm_file_name('test.asm')
