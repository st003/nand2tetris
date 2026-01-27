import unittest
from pathlib import Path

import tokens as T
from exceptions import SymbolTableError
from file_util import is_jack_file
from lexical_elements import get_token
from SymbolTable import SymbolTable

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

    def test_symbol_table_counter(self):
        """Tests a symbol's index does not change as the counter does."""
        st = SymbolTable()
        st.define('test', 'int', 'static')
        self.assertEqual(st._class_scope['test']['index'], 0)
        self.assertEqual(st._static_count, 1)

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

