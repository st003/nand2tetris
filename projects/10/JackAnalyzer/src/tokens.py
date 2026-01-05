from constants import TOKEN_TYPE
from exceptions import JackTokenizerError

class BaseToken():
    """Base class for all Tokens."""

    def __init__(self, value=''):
        self.value = value
        self.type = 'token'

    def get_xml_value(self):
        """Returns the token's value formatted for xml."""
        return f' {self.value} '

class IdentifierToken(BaseToken):
    """Class, method, function, or variable names."""

    def __init__(self, value):

        # first char cannot be a number
        try:
            int(value[0])
            raise JackTokenizerError(f"Identifier '{value}' cannot begin with an integer")
        except ValueError:
            # failure to convert the first char to a int is good
            pass

        # must contain only alphanumeric and/or underscores
        for c in value:
            if not c.isalnum() and c != '_':
                raise JackTokenizerError(f"Identifier '{value}' contains illegal characters")

        self.value = value
        self.type = TOKEN_TYPE.IDENTIFIER

class IntegerConstantToken(BaseToken):
    """Integers from 0-32767."""

    MIN = 0
    MAX = 32767

    def __init__(self, value):
        self.value = value
        self.type = TOKEN_TYPE.INTEGER_CONSTANT

    @staticmethod
    def is_integer_token(value):
        try:
            as_int = int(value)
            if as_int < IntegerConstantToken.MIN or as_int > IntegerConstantToken.MAX:
                return False
            return True
        except ValueError:
            return False

class KeywordToken(BaseToken):
    """One of the language defined keywords."""

    def __init__(self, value):
        self.value = value
        self.type = TOKEN_TYPE.KEYWORD

class StringConstantToken(BaseToken):
    """A sequence of chars bounded by double-quotes."""

    def __init__(self, value):
        self.value = value
        self.type = TOKEN_TYPE.STRING_CONSTANT

class SymbolToken(BaseToken):
    """One of the language defined symbols."""

    xml_esc = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;'
    }

    def __init__(self, value):
        self.value = value
        self.type = TOKEN_TYPE.SYMBOL

    def get_xml_value(self):
        """Returns the token's value formatted for xml."""
        if self.value in self.xml_esc:
            return f' {self.xml_esc[self.value]} '
        else:
            return super().get_xml_value()
