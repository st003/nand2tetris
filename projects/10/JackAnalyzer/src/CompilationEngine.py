import xml.etree.ElementTree as ET

from constants import TOKEN_TYPE
from exceptions import CompilationEngineError
from JackTokenizer import JackTokenizer
from xml_formatter import make_pretty

class CompilationEngine():
    """Class for lexing and parsing Jack source code."""

    def __init__(self, jack_file_path, debug=False):

        self.parent_dir = jack_file_path.parent
        self.file_name = jack_file_path.stem
        self.debug = debug

        self.tokenizer = JackTokenizer(jack_file_path, debug)

        # store the etree as a stack so the final xml is not flat
        self.internal_etree_stack = [ET.Element('class')]

    def get_output_file_path(self):
        """
        Returns the output file path inserting a debug string when the debug
        flag is set.
        """
        if self.debug:
            return f'{self.parent_dir}/{self.file_name}_DEBUG.xml'
        return f'{self.parent_dir}/{self.file_name}.xml'

    def add_token_to_xml(self, sub_element=None):
        """
        Inserts the current token into the internal XML etree.

        Creates a new sub-element first if defined.
        """

        if sub_element is not None:
            new_sub_element = ET.SubElement(self.internal_etree_stack[-1], sub_element)
            # push onto the stack so subsequent elements are nested
            self.internal_etree_stack.append(new_sub_element)

        if self.tokenizer.current_token is not None:
            # always use the top of the stack
            new_token = ET.SubElement(self.internal_etree_stack[-1], self.tokenizer.current_token.type)
            new_token.text = self.tokenizer.current_token.get_xml_value()

    def write_xml(self):
        """
        Creates XML files from the tokenizer and the CompilationEngine
        internal etrees.
        """

        # first write the tokenizer's XML
        self.tokenizer.write_xml()

        # now write the CompilationEngine's XML
        # get the root element of the etree which is always at the bottom of the stack
        xml_tree = ET.ElementTree(self.internal_etree_stack[0])
        xml_text = make_pretty(xml_tree, indent=2)
        try:
            with open(self.get_output_file_path(), 'w') as output_file:
                output_file.write(xml_text)
        except Exception as error:
            raise CompilationEngineError(f"Unable to create XML class file at: '{self.get_output_file_path()}'") from error

    def eat_token_by_value(self, value):
        """Advances to the next token and checks its value."""
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            if self.tokenizer.current_token.value != value:
                raise CompilationEngineError(f"CompilationEngine.eat_token_by_value() expected '{value}' but got '{self.tokenizer.current_token.value}'")
        else:
            raise CompilationEngineError('Tokenizer has reached the end of the file')

    def eat_token_by_type(self, type):
        """Advances to the next token and checks its type."""
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            if self.tokenizer.tokenType() != type:
                raise CompilationEngineError(f"CompilationEngine.eat_token_by_type() expected '{type}' but got '{self.tokenizer.tokenType()}'")
        else:
            raise CompilationEngineError('Tokenizer has reached the end of the file')

    def eat_token_in(self, set):
        """Advances to the next token and checks its category."""
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            return (self.tokenizer.current_token.value in set)
        else:
            raise CompilationEngineError('Tokenizer has reached the end of the file')

    # TODO: definitions found at:
    # 4.5 @2:19
    # 4.8 @12:50+

    def compileClass(self):
        """Parses and compiles a Class declaration."""

        self.eat_token_by_value('class')
        self.add_token_to_xml()

        self.eat_token_by_type(TOKEN_TYPE.IDENTIFIER)
        self.add_token_to_xml()

        self.eat_token_by_value('{')
        self.add_token_to_xml()

        # TODO: call n-number of complileClassVarDec()

        while self.eat_token_in({'constructor', 'function', 'method'}):
            self.complileSubroutineDec()

        # TODO: uncomment after all other compile methods are implemented
        # self.eat_token_by_value('}')
        # self.add_token_to_xml()

    def complileClassVarDec(self):
        """."""
        # TODO: implement
        pass

    def complileSubroutineDec(self):
        """Parses and compiles a sub-routine declaration."""

        self.add_token_to_xml('subroutineDec')

        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            if (self.tokenizer.current_token.value in {'void', 'int', 'char', 'boolean'}
                or self.tokenizer.tokenType() == TOKEN_TYPE.IDENTIFIER):
                self.add_token_to_xml()
            else:
                raise CompilationEngineError(f"{self.tokenizer.current_token.value} is not a valid sub-routine return type")
        else:
            raise CompilationEngineError('Tokenizer has reached the end of the file')

        self.eat_token_by_type(TOKEN_TYPE.IDENTIFIER)
        self.add_token_to_xml()

        self.eat_token_by_value('(')
        self.add_token_to_xml()

        # TODO: implement complileParameterList()

        # self.eat_token_by_value(')')
        # self.add_token_to_xml()

        # TODO: implement complileSubroutineBody()
        # TODO: pop the etree stack

    def complileParameterList(self):
        """."""
        # TODO: implement
        pass

    def complileSubroutineBody(self):
        """."""
        # TODO: implement
        pass

    def complileVarDec(self):
        """."""
        # TODO: implement
        pass

    def complileStatements(self):
        """."""
        # TODO: implement
        pass

    def complileLet(self):
        """."""
        # TODO: implement
        pass

    def complileIf(self):
        """."""
        # TODO: implement
        pass

    def complileWhile(self):
        """."""
        # TODO: implement
        pass

    def complileDo(self):
        """."""
        # TODO: implement
        pass

    def complileReturn(self):
        """."""
        # TODO: implement
        pass

    def complileExpression(self):
        """."""
        # TODO: implement
        pass

    def complileTerm(self):
        """."""
        # TODO: implement
        pass

    def complileExpressionList(self):
        """."""
        # TODO: implement
        pass
