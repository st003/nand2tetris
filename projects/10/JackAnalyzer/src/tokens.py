from constants import TOKEN_TYPE

class BaseToken():
    """Base class for all Tokens."""

    def __init__(self, identifier=''):
        self.identifier = identifier
        self.type = 'token'

    def get_xml_value(self):
        """Returns the token's identifier formatted for xml."""
        return f' {self.identifier} '

class KeywordToken(BaseToken):

    def __init__(self, identifier):
        self.identifier = identifier
        self.type = TOKEN_TYPE.KEYWORD

class SymbolToken(BaseToken):

    def __init__(self, identifier):
        self.identifier = identifier
        self.type = TOKEN_TYPE.SYMBOL
