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
        self.type = 'keyword'

class SymbolToken(BaseToken):

    def __init__(self, value):
        self.value = value
        self.type = 'symbol'
