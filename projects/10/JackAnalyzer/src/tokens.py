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

class KeywordToken(BaseToken):

    def __init__(self, value):
        self.value = value
        self.type = TOKEN_TYPE.KEYWORD

class SymbolToken(BaseToken):

    def __init__(self, value):
        self.value = value
        self.type = TOKEN_TYPE.SYMBOL

class IdentifierToken(BaseToken):

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

# TODO: add string constant
# TODO: add integer constant
