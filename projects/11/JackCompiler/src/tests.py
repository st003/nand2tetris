import unittest
from pathlib import Path

import tokens as T
from exceptions import SymbolTableError
from file_util import is_jack_file
from JackCompiler import validate_flags
from lexical_elements import get_token
from SymbolTable import SymbolTable

class TestJackCompiler(unittest.TestCase):

    def test_validate_flags_success(self):
        """Tests all legal combinations of flags."""
        output = validate_flags('-dv')
        self.assertTrue(output)
        output = validate_flags('-dv')
        self.assertTrue(output)
        output = validate_flags('-d')
        self.assertTrue(output)
        output = validate_flags('-v')
        self.assertTrue(output)

    def test_validate_flags_failure(self):
        """Tests validate_flags fail conditions."""
        output = validate_flags('d')
        self.assertFalse(output)
        output = validate_flags('x')
        self.assertFalse(output)

class TestFileUtil(unittest.TestCase):

    def test_is_jack_file_success(self):
        """Returns True when file extention is '.jack'."""
        file_path = Path('myFile.jack')
        output = is_jack_file(file_path)
        self.assertTrue(output)

    def test_is_jack_file_fail(self):
        """Returns False when file extention is not '.jack'."""
        file_path = Path('myFile.xml')
        output = is_jack_file(file_path)
        self.assertFalse(output)

class TestLexer(unittest.TestCase):

    def test_get_token_keyword(self):
        """Returns a keyword token."""
        output = get_token('class')
        self.assertIsInstance(output, T.KeywordToken)

    def test_get_token_symbol(self):
        """Returns a symbol token."""
        output = get_token('(')
        self.assertIsInstance(output, T.SymbolToken)

    def test_get_token_integer_constant(self):
        """Returns an integer constant token."""
        output = get_token('1')
        self.assertIsInstance(output, T.IntegerConstantToken)

    def test_get_token_identifier(self):
        """Returns an identifier token."""
        output = get_token('MyClass')
        self.assertIsInstance(output, T.IdentifierToken)

class TestTokens(unittest.TestCase):

    def test_is_integer_token_success(self):
        """Verifies an integer string can be converted into an integer constant token."""
        output = T.IntegerConstantToken.is_integer_token('10')
        self.assertTrue(output)

    def test_is_integer_token_not_int(self):
        """Check a letter string cannot be converted into an integer constant token."""
        output = T.IntegerConstantToken.is_integer_token('a')
        self.assertFalse(output)

    def test_is_integer_token_less_than_min(self):
        """Verifies an integer constant is not less than the min value."""
        value = str(T.IntegerConstantToken.MIN - 1)
        output = T.IntegerConstantToken.is_integer_token(value)
        self.assertFalse(output)

    def test_is_integer_token_greater_than_max(self):
        """Verifies an integer constant is not greater than the max value."""
        value = str(T.IntegerConstantToken.MAX + 1)
        output = T.IntegerConstantToken.is_integer_token(value)
        self.assertFalse(output)

class TestSymbolTable(unittest.TestCase):

    def test_symbol_table_counter(self):
        """Tests a symbol's index does not change as the counter does."""
        st = SymbolTable()
        st.define('test', 'int', 'static')
        self.assertEqual(st._class_scope['test']['index'], 0)
        self.assertEqual(st._static_count, 1)

    def test_symbol_table_VarCount_success(self):
        """Tests a valid case of VarCount."""

        st = SymbolTable()
        st.define('static1', 'int', 'static')
        st.define('field1', 'int', 'field')
        st.define('field2', 'int', 'field')
        st.define('arg1', 'int', 'argument')
        st.define('arg2', 'int', 'argument')
        st.define('arg3', 'int', 'argument')
        st.define('local1', 'int', 'local')
        st.define('local2', 'int', 'local')
        st.define('local3', 'int', 'local')
        st.define('local4', 'int', 'local')

        actual = st.VarCount('static')
        self.assertEqual(actual, 1)
        actual = st.VarCount('field')
        self.assertEqual(actual, 2)
        actual = st.VarCount('argument')
        self.assertEqual(actual, 3)
        actual = st.VarCount('local')
        self.assertEqual(actual, 4)

    def test_symbol_table_VarCount_fail(self):
        """Tests an invalid case of VarCount."""
        st = SymbolTable()
        st.define('static1', 'int', 'static')
        with self.assertRaises(SymbolTableError):
            st.VarCount('none')

    def test_symbol_table_KindOf_success(self):
        """Tests a valid use case of KindOf."""
        st = SymbolTable()
        st.define('test', 'int', 'static')
        actual = st.KindOf('test')
        self.assertEqual(actual, 'static')

    def test_symbol_table_KindOf_fail(self):
        """Tests an error use case of KindOf."""
        st = SymbolTable()
        st.define('test', 'int', 'static')
        with self.assertRaises(SymbolTableError):
            st.KindOf('none')

    def test_symbol_table_TypeOf_success(self):
        """Tests a valid use case of TypeOf."""
        st = SymbolTable()
        st.define('test', 'int', 'static')
        actual = st.TypeOf('test')
        self.assertEqual(actual, 'int')

    def test_symbol_table_TypeOf_fail(self):
        """Tests an error use case of TypeOf."""
        st = SymbolTable()
        st.define('test', 'int', 'static')
        with self.assertRaises(SymbolTableError):
            st.TypeOf('none')

    def test_symbol_table_IndexOf_success(self):
        """Tests a valid use case of IndexOf."""
        st = SymbolTable()
        st.define('test', 'int', 'static')
        actual = st.IndexOf('test')
        self.assertEqual(actual, 0)

    def test_symbol_table_IndexOf_fail(self):
        """Tests an error use case of IndexOf."""
        st = SymbolTable()
        st.define('test', 'int', 'static')
        with self.assertRaises(SymbolTableError):
            st.IndexOf('none')
