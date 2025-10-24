import unittest

import instructions as ins
from exceptions import ParseError, VMTranslatorError
from parser import parse_instruction
from translator import skip_line
from utils import get_vm_file_name

class TestInstructions(unittest.TestCase):

    def test_get_memory_segment(self):
        """Verify the memory segment is selected."""
        bi = ins.MemoryInstruction(1, ['push', 'constant', '1'])
        output = bi.get_memory_segment()
        self.assertEqual(output, 'constant')

    def test_get_offset(self):
        """Verify the offset is selected."""
        bi = ins.MemoryInstruction(1, ['push', 'constant', '1'])
        output = bi.get_offset()
        self.assertEqual(output, '1')

    def test_get_comment(self):
        """Verify the comment is correct."""
        bi = ins.MemoryInstruction(1, ['push', 'constant', '1'])
        output = bi.get_comment()
        self.assertEqual(output, '// push constant 1')

class TestParser(unittest.TestCase):

    def test_parse_instruction_two_parts(self):
        """The instruction has two parts."""
        with self.assertRaises(ParseError):
            parse_instruction(1, 'one two')

    def test_parse_instruction_add(self):
        """Test add command"""
        output = parse_instruction(1, 'add')
        self.assertIsInstance(output, ins.AddInstruction)

    def test_parse_instruction_sub(self):
        """Test sub command"""
        output = parse_instruction(1, 'sub')
        self.assertIsInstance(output, ins.SubInstruction)

    def test_parse_instruction_neg(self):
        """Test neg command"""
        output = parse_instruction(1, 'neg')
        self.assertIsInstance(output, ins.NegInstruction)

    def test_parse_instruction_eq(self):
        """Test eq command"""
        output = parse_instruction(1, 'eq')
        self.assertIsInstance(output, ins.EqInstruction)

    def test_parse_instruction_gt(self):
        """Test gt command"""
        output = parse_instruction(1, 'gt')
        self.assertIsInstance(output, ins.GtInstruction)

    def test_parse_instruction_lt(self):
        """Test lt command"""
        output = parse_instruction(1, 'lt')
        self.assertIsInstance(output, ins.LtInstruction)

    def test_parse_instruction_and(self):
        """Test and command"""
        output = parse_instruction(1, 'and')
        self.assertIsInstance(output, ins.AndInstruction)

    def test_parse_instruction_or(self):
        """Test or command"""
        output = parse_instruction(1, 'or')
        self.assertIsInstance(output, ins.OrInstruction)

    def test_parse_instruction_not(self):
        """Test not command"""
        output = parse_instruction(1, 'not')
        self.assertIsInstance(output, ins.NotInstruction)

    def test_parse_instruction_invalid_single_command(self):
        """Invalid arithmetic/logical instruction."""
        with self.assertRaises(ParseError):
            parse_instruction(1, 'fake')

    def test_parse_instruction_push(self):
        """Test push command"""
        output = parse_instruction(1, 'push static 1')
        self.assertIsInstance(output, ins.PushInstruction)

    def test_parse_instruction_pop(self):
        """Test pop command"""
        output = parse_instruction(1, 'pop static 1')
        self.assertIsInstance(output, ins.PopInstruction)

    def test_parse_instruction_invalid_memory_command(self):
        """Invalid memory instruction."""
        with self.assertRaises(ParseError):
            parse_instruction(1, 'fake static 1')

    def test_parse_instruction_invalid_memory_segment(self):
        """Invalid memory segment."""
        with self.assertRaises(ParseError):
            parse_instruction(1, 'push fake 1')

    def test_parse_instruction_invalid_offset_character(self):
        """Invalid offset character."""
        with self.assertRaises(ParseError):
            parse_instruction(1, 'push fake a')

    def test_parse_instruction_invalid_offset_number(self):
        """Invalid offset character number."""
        with self.assertRaises(ParseError):
            parse_instruction(1, 'push constant -1')

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
