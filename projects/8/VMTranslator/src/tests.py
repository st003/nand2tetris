import unittest
from pathlib import Path

import instructions as ins
from exceptions import ParseError, TranslationError, VMTranslatorError
from file_util import get_input_lines, get_vm_files, Line
from parser import check_offset, parse_instruction, tokenize

class TestInstructions(unittest.TestCase):

    def test_get_comment(self):
        """Verify the comment is correct."""
        bi = parse_instruction(Line('test', 'push constant 1'))
        output = bi.get_comment()
        self.assertEqual(output, '// push constant 1')

    def test_get_pointer_push_invalid_offset(self):
        """Verify error checking in push pointer."""
        with self.assertRaises(TranslationError):
            parse_instruction(Line('test', 'push pointer 5'))

    def test_get_pointer_pop_invalid_offset(self):
        """Verify error checking in pop pointer."""
        with self.assertRaises(TranslationError):
            parse_instruction(Line('test', 'pop pointer 5'))

class TestParser(unittest.TestCase):

    def test_tokenize(self):
        """Test tokenize."""
        tokens = tokenize('push constant 1')
        self.assertTrue(len(tokens) == 3)

    def test_tokenize_inline_comment(self):
        """Test tokenize inline comments."""
        tokens = tokenize('add // inline')
        self.assertTrue(len(tokens) == 1)

    def test_tokenize_whitespace(self):
        """Test line with extra whitespace in between tokens."""
        tokens = tokenize('label  TEST')
        self.assertTrue(len(tokens) == 2)

    def test_tokenize_tabs(self):
        """Test line with tabs."""
        tokens = tokenize('label\tTEST')
        self.assertTrue(len(tokens) == 2)

    def test_check_offset_not_number(self):
        """Invalid offset value."""
        with self.assertRaises(ParseError):
            check_offset(Line('test', 'push constant a'), 'a')

    def test_check_offset_negative_number(self):
        """Negative offset value."""
        with self.assertRaises(ParseError):
            check_offset(Line('test', 'push constant -1'), '-1')

    def test_parse_instruction_inline_comment(self):
        """Test inline comment"""
        output = parse_instruction(Line('test', 'add // comment'))
        self.assertIsInstance(output, ins.AddInstruction)

    def test_parse_instruction_add(self):
        """Test add command"""
        output = parse_instruction(Line('test', 'add'))
        self.assertIsInstance(output, ins.AddInstruction)

    def test_parse_instruction_sub(self):
        """Test sub command"""
        output = parse_instruction(Line('test', 'sub'))
        self.assertIsInstance(output, ins.SubInstruction)

    def test_parse_instruction_neg(self):
        """Test neg command"""
        output = parse_instruction(Line('test', 'neg'))
        self.assertIsInstance(output, ins.NegInstruction)

    def test_parse_instruction_eq(self):
        """Test eq command"""
        output = parse_instruction(Line('test', 'eq'))
        self.assertIsInstance(output, ins.EqInstruction)

    def test_parse_instruction_gt(self):
        """Test gt command"""
        output = parse_instruction(Line('test', 'gt'))
        self.assertIsInstance(output, ins.GtInstruction)

    def test_parse_instruction_lt(self):
        """Test lt command"""
        output = parse_instruction(Line('test', 'lt'))
        self.assertIsInstance(output, ins.LtInstruction)

    def test_parse_instruction_and(self):
        """Test and command"""
        output = parse_instruction(Line('test', 'and'))
        self.assertIsInstance(output, ins.AndInstruction)

    def test_parse_instruction_or(self):
        """Test or command"""
        output = parse_instruction(Line('test', 'or'))
        self.assertIsInstance(output, ins.OrInstruction)

    def test_parse_instruction_not(self):
        """Test not command"""
        output = parse_instruction(Line('test', 'not'))
        self.assertIsInstance(output, ins.NotInstruction)

    def test_parse_instruction_invalid_single_command(self):
        """Invalid arithmetic/logical instruction."""
        with self.assertRaises(ParseError):
            parse_instruction(Line('test', 'fake'))

    def test_parse_instruction_goto(self):
        """Test goto command"""
        output = parse_instruction(Line('test', 'goto LABEL'))
        self.assertIsInstance(output, ins.GotoInstruction)

    def test_parse_instruction_ifgoto(self):
        """Test if-goto command"""
        output = parse_instruction(Line('test', 'if-goto LABEL'))
        self.assertIsInstance(output, ins.IfGotoInstruction)

    def test_parse_instruction_label(self):
        """Test label command"""
        output = parse_instruction(Line('test', 'label LABEL'))
        self.assertIsInstance(output, ins.LabelInstruction)

    def test_parse_instruction_invalid_branching_command(self):
        """Invalid branching instruction."""
        with self.assertRaises(ParseError):
            parse_instruction(Line('test', 'fake command'))

    def test_parse_instruction_call(self):
        """Test call command"""
        output = parse_instruction(Line('test', 'call MyFunc 1'))
        self.assertIsInstance(output, ins.CallInstruction)

    def test_parse_instruction_function(self):
        """Test function command"""
        output = parse_instruction(Line('test', 'function MyFunc 2'))
        self.assertIsInstance(output, ins.FunctionInstruction)

    def test_parse_instruction_return(self):
        """Test return command"""
        output = parse_instruction(Line('test', 'return'))
        self.assertIsInstance(output, ins.ReturnInstruction)

    def test_parse_instruction_push(self):
        """Test push command"""
        output = parse_instruction(Line('test', 'push static 1'))
        self.assertIsInstance(output, ins.PushInstruction)

    def test_parse_instruction_pop(self):
        """Test pop command"""
        output = parse_instruction(Line('test', 'pop static 1'))
        self.assertIsInstance(output, ins.PopInstruction)

    def test_parse_instruction_invalid_memory_command(self):
        """Invalid memory instruction."""
        with self.assertRaises(ParseError):
            parse_instruction(Line('test', 'fake static 1'))

    def test_parse_instruction_invalid_memory_segment(self):
        """Invalid memory segment."""
        with self.assertRaises(ParseError):
            parse_instruction(Line('test', 'push fake 1'))

    def test_parse_instruction_invalid_offset_character(self):
        """Invalid offset character."""
        with self.assertRaises(ParseError):
            parse_instruction(Line('test', 'push fake a'))

    def test_parse_instruction_invalid_offset_number(self):
        """Invalid offset character number."""
        with self.assertRaises(ParseError):
            parse_instruction(Line('test', 'push constant -1'))

    def test_parse_instruction_function_invalid_offset_number(self):
        """Invalid function offset character number."""
        with self.assertRaises(ParseError):
            parse_instruction(Line('test', 'function myfunction -1'))

class TestFileUtil(unittest.TestCase):

    def test_line_is_empty(self):
        """Test lines with no content."""
        l = Line('test', '\n')
        self.assertTrue(l.is_empty())

    def test_line_is_comment(self):
        """Test comment line."""
        l = Line('test', '// comment')
        self.assertTrue(l.is_comment())

    def test_get_input_lines_success_NestedCall(self):
        """Test get_input_lines returns data from NestedCall/Sys.vm."""
        paths = [Path('../../test_files/NestedCall/Sys.vm')]
        lines, count = get_input_lines(paths)
        self.assertTrue(len(lines) > 0)
        self.assertTrue(count == 1)

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
