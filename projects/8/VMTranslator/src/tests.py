import unittest

import instructions as ins
from exceptions import ParseError, TranslationError, VMTranslatorError
from parser import check_offset, parse_instruction
from translator import skip_line
from utils import get_vm_files

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

    def test_get_pointer_push_invalid_offset(self):
        """Verify error checking in push pointer."""
        with self.assertRaises(TranslationError):
            ins.PushInstruction(1, ['push', 'pointer', '5'])

    def test_get_pointer_pop_invalid_offset(self):
        """Verify error checking in pop pointer."""
        with self.assertRaises(TranslationError):
            ins.PopInstruction(1, ['pop', 'pointer', '5'])

class TestParser(unittest.TestCase):

    def test_check_offset_not_number(self):
        """Invalid offset value."""
        with self.assertRaises(ParseError):
            check_offset(1, 'push constant a', 'a')

    def test_check_offset_negative_number(self):
        """Negative offset value."""
        with self.assertRaises(ParseError):
            check_offset(1, 'push constant -1', '-1')

    def test_parse_instruction_inline_comment(self):
        """Test inline comment"""
        output = parse_instruction(1, 'add // comment')
        self.assertIsInstance(output, ins.AddInstruction)

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

    def test_parse_instruction_goto(self):
        """Test goto command"""
        output = parse_instruction(1, 'goto LABEL')
        self.assertIsInstance(output, ins.GotoInstruction)

    def test_parse_instruction_ifgoto(self):
        """Test if-goto command"""
        output = parse_instruction(1, 'if-goto LABEL')
        self.assertIsInstance(output, ins.IfGotoInstruction)

    def test_parse_instruction_label(self):
        """Test label command"""
        output = parse_instruction(1, 'label LABEL')
        self.assertIsInstance(output, ins.LabelInstruction)

    def test_parse_instruction_invalid_branching_command(self):
        """Invalid branching instruction."""
        with self.assertRaises(ParseError):
            parse_instruction(1, 'fake command')

    def test_parse_instruction_call(self):
        """Test call command"""
        output = parse_instruction(1, 'call MyFunc 1')
        self.assertIsInstance(output, ins.CallInstruction)

    def test_parse_instruction_function(self):
        """Test function command"""
        output = parse_instruction(1, 'function MyFunc 2')
        self.assertIsInstance(output, ins.FunctionInstruction)

    def test_parse_instruction_return(self):
        """Test return command"""
        output = parse_instruction(1, 'return')
        self.assertIsInstance(output, ins.ReturnInstruction)

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

    def test_parse_instruction_function_invalid_offset_number(self):
        """Invalid function offset character number."""
        with self.assertRaises(ParseError):
            parse_instruction(1, 'function myfunction -1')

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

    def test_get_vm_files_success_StaticsTest(self):
        """Test get_vm_files with StaticsTest."""
        vm_files, output_file_path = get_vm_files('../../test_files/StaticsTest')
        self.assertEqual(len(vm_files), 3)
        self.assertEqual(output_file_path, '../../test_files/StaticsTest.asm')

    def test_get_vm_files_success_BasicLoop(self):
        """Test get_vm_files with BasicLoop."""
        vm_files, output_file_path = get_vm_files('../../test_files/BasicLoop.vm')
        self.assertEqual(len(vm_files), 1)
        self.assertEqual(str(vm_files[0]), '../../test_files/BasicLoop.vm')
        self.assertEqual(output_file_path, '../../test_files/BasicLoop.asm')

    def test_get_vm_file_name_missing_extension(self):
        """Missing file extension."""
        with self.assertRaises(VMTranslatorError):
            get_vm_files('missing-ext')

    def test_get_vm_file_name_wrong_extension(self):
        """Incorrect file extension."""
        with self.assertRaises(VMTranslatorError):
            get_vm_files('wrong-ext.asm')
