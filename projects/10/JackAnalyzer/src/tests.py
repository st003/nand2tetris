import unittest
from pathlib import Path

from file_util import is_jack_file
from lexical_elements import get_token
import tokens as T

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
        """."""
        output = get_token('class')
        self.assertIsInstance(output, T.KeywordToken)

    def test_get_token_symbol(self):
        """."""
        output = get_token('(')
        self.assertIsInstance(output, T.SymbolToken)

    def test_get_token_integer_constant(self):
        """."""
        output = get_token('1')
        self.assertIsInstance(output, T.IntegerConstantToken)

    def test_get_token_identifier(self):
        """."""
        output = get_token('MyClass')
        self.assertIsInstance(output, T.IdentifierToken)

    def test_is_integer_token_success(self):
        """."""
        output = T.IntegerConstantToken.is_integer_token('1')
        self.assertTrue(output)

    def test_is_integer_token_not_int(self):
        """."""
        output = T.IntegerConstantToken.is_integer_token('a')
        self.assertFalse(output)

    def test_is_integer_token_less_than_min(self):
        """."""
        value = str(T.IntegerConstantToken.MIN - 1)
        output = T.IntegerConstantToken.is_integer_token(value)
        self.assertFalse(output)

    def test_is_integer_token_greater_than_max(self):
        """."""
        value = str(T.IntegerConstantToken.MAX + 1)
        output = T.IntegerConstantToken.is_integer_token(value)
        self.assertFalse(output)
