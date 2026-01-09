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

    def add_current_token_to_xml(self):
        """Inserts the current token into the internal XML etree."""
        if self.tokenizer.current_token is not None:
            # always use the top of the stack
            new_token = ET.SubElement(self.internal_etree_stack[-1], self.tokenizer.current_token.type)
            new_token.text = self.tokenizer.current_token.get_xml_value()

    def add_sub_element_to_xml(self, name):
        """Creates a new sub-element in the xml and move it to the top of the etree stack."""
        if name is not None:
            new_sub_element = ET.SubElement(self.internal_etree_stack[-1], name)
            # push onto the stack so subsequent elements are nested
            self.internal_etree_stack.append(new_sub_element)

    def insert_xml_empty_escape_string(self):
        """XML formatting helper for ensuring tags follow the <xml><xml/> format instead of </xml>."""
        self.internal_etree_stack[-1].text = '__XML_EMPTY__'

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
        except OSError as error:
            raise IOError(f"Unable to create XML class file at: '{self.get_output_file_path()}'") from error

    def get_current_token_value(self):
        """Returns the text value of the current token."""
        if self.tokenizer.current_token is not None:
            return self.tokenizer.current_token.value
        return None

    def eat_token_by_value(self, value):
        """Advances to the next token and checks its value."""
        self.tokenizer.advance()
        if self.get_current_token_value() != value:
            raise CompilationEngineError(self.tokenizer, f"CompilationEngine.eat_token_by_value() expected '{value}' but got '{self.get_current_token_value()}'")
        self.add_current_token_to_xml()

    def eat_token_by_type(self, type):
        """Advances to the next token and checks its type."""
        self.tokenizer.advance()
        if self.tokenizer.tokenType() != type:
            raise CompilationEngineError(self.tokenizer, f"CompilationEngine.eat_token_by_type() expected '{type}' but got '{self.tokenizer.tokenType()}'")
        self.add_current_token_to_xml()

    def token_is_type(self, token):
        """Check if the current token is valid return type."""
        # NOTE: technically 'identifier' is not enough to prove it's a class definition
        return (token.value in {'int', 'char', 'boolean'}
                or token.type == TOKEN_TYPE.IDENTIFIER)

    def compileClass(self):
        """Parses a class declaration."""

        self.eat_token_by_value('class')
        self.eat_token_by_type(TOKEN_TYPE.IDENTIFIER)
        self.eat_token_by_value('{')

        while True:
            if self.complileClassVarDec():
                continue
            break

        while True:
            if self.complileSubroutineDec():
                continue
            break

        self.eat_token_by_value('}')

    def complileClassVarDec(self):
        """Parses a class variable declaration."""

        next_token = self.tokenizer.peek_next_token()
        if next_token.value not in {'static', 'field'}:
            return False

        self.add_sub_element_to_xml('classVarDec')
        self.tokenizer.advance()
        self.add_current_token_to_xml()

        # type
        next_token = self.tokenizer.peek_next_token()
        if self.token_is_type(next_token):
            self.tokenizer.advance()
            self.add_current_token_to_xml()
        else:
            raise CompilationEngineError(self.tokenizer, f"{next_token.value} is not a valid type")

        # 1+ variable names separated by ','
        self.eat_token_by_type(TOKEN_TYPE.IDENTIFIER)
        while True:
            next_token = self.tokenizer.peek_next_token()
            if next_token.value != ',':
                break
            self.eat_token_by_value(',')
            self.eat_token_by_type(TOKEN_TYPE.IDENTIFIER)

        self.eat_token_by_value(';')

        self.internal_etree_stack.pop()
        return True

    def complileSubroutineDec(self):
        """Parses a sub-routine declaration."""

        next_token = self.tokenizer.peek_next_token()
        if next_token.value not in {'constructor', 'function', 'method'}:
            return False

        self.add_sub_element_to_xml('subroutineDec')
        self.tokenizer.advance()
        self.add_current_token_to_xml()

        next_token = self.tokenizer.peek_next_token()
        if next_token.value == 'void' or self.token_is_type(next_token):
            self.tokenizer.advance()
            self.add_current_token_to_xml()
        else:
            raise CompilationEngineError(self.tokenizer, f"{next_token.value} is not a valid sub-routine return type")

        self.eat_token_by_type(TOKEN_TYPE.IDENTIFIER)
        self.eat_token_by_value('(')
        self.complileParameterList()
        self.eat_token_by_value(')')
        self.complileSubroutineBody()

        self.internal_etree_stack.pop()
        return True

    def complileParameterList(self):
        """Parses a parameter list."""

        self.add_sub_element_to_xml('parameterList')

        next_token = self.tokenizer.peek_next_token()
        if self.token_is_type(next_token):

            self.tokenizer.advance() # this is the type
            self.add_current_token_to_xml()
            self.eat_token_by_type(TOKEN_TYPE.IDENTIFIER)

            while True:
                next_token = self.tokenizer.peek_next_token()
                if next_token.value != ',':
                    break
                self.eat_token_by_value(',')
                self.tokenizer.advance() # this is the type
                self.add_current_token_to_xml()
                self.eat_token_by_type(TOKEN_TYPE.IDENTIFIER)

        else:
            self.insert_xml_empty_escape_string()

        self.internal_etree_stack.pop()

    def complileSubroutineBody(self):
        """Parses a sub-routine body."""

        self.add_sub_element_to_xml('subroutineBody')
        self.eat_token_by_value('{')

        # variable declarations
        while True:
            if self.complileVarDec():
                continue
            break

        # statements
        self.complileStatements()

        self.eat_token_by_value('}')

        self.internal_etree_stack.pop()

    def complileVarDec(self):
        """Parses a var declaration."""

        next_token = self.tokenizer.peek_next_token()
        if next_token.value != 'var':
            return False

        self.add_sub_element_to_xml('varDec')
        self.eat_token_by_value('var')

        next_token = self.tokenizer.peek_next_token()
        if self.token_is_type(next_token):
            self.tokenizer.advance()
            self.add_current_token_to_xml()
        else:
            raise CompilationEngineError(self.tokenizer, f"{next_token.value} is not a valid type")

        # get 1 or more variable names
        self.eat_token_by_type(TOKEN_TYPE.IDENTIFIER)
        while True:
            next_token = self.tokenizer.peek_next_token()
            if next_token.value == ',':
                self.eat_token_by_value(',')
                self.eat_token_by_type(TOKEN_TYPE.IDENTIFIER)
            elif next_token.value == ';':
                self.eat_token_by_value(';')
                break
            else:
                raise CompilationEngineError(self.tokenizer, f"Expected ',' or ';' not '{next_token.value}'")

        self.internal_etree_stack.pop()
        return True

    def complileStatements(self):
        """Parses all statements by type."""

        self.add_sub_element_to_xml('statements')

        next_token = self.tokenizer.peek_next_token()

        if next_token.value not in {'let', 'if', 'while', 'do', 'return'}:
            self.insert_xml_empty_escape_string()
            self.internal_etree_stack.pop()
            return

        while True:

            if next_token.value == 'let':
                self.complileLet()
            elif next_token.value == 'if':
                self.complileIf()
            elif next_token.value == 'while':
                self.complileWhile()
            elif next_token.value == 'do':
                self.complileDo()
            elif next_token.value == 'return':
                self.complileReturn()

            next_token = self.tokenizer.peek_next_token()
            if next_token.value not in {'let', 'if', 'while', 'do', 'return'}:
                break

        self.internal_etree_stack.pop()

    def complileLet(self):
        """Parses a let statement."""

        self.add_sub_element_to_xml('letStatement')
        self.eat_token_by_value('let')
        self.eat_token_by_type(TOKEN_TYPE.IDENTIFIER)

        next_token = self.tokenizer.peek_next_token()
        if next_token.value == '[':
            self.eat_token_by_value('[')
            self.complileExpression()
            self.eat_token_by_value(']')
            self.eat_token_by_value('=')

        elif next_token.value == '=':
            self.eat_token_by_value('=')

        else:
            raise CompilationEngineError(self.tokenizer, f"CompilationEngine.complileLet() expected '[' or '=' but got '{next_token.value}'")

        self.complileExpression()
        self.eat_token_by_value(';')

        self.internal_etree_stack.pop()

    def complileIf(self):
        """Parses an if statement."""

        self.add_sub_element_to_xml('ifStatement')
        self.eat_token_by_value('if')
        self.eat_token_by_value('(')
        self.complileExpression()
        self.eat_token_by_value(')')
        self.eat_token_by_value('{')
        self.complileStatements()
        self.eat_token_by_value('}')

        # 0+ else
        next_token = self.tokenizer.peek_next_token()
        if next_token.value == 'else':
            self.eat_token_by_value('else')
            self.eat_token_by_value('{')
            self.complileStatements()
            self.eat_token_by_value('}')

        self.internal_etree_stack.pop()

    def complileWhile(self):
        """Parses a while statement."""
        self.add_sub_element_to_xml('whileStatement')
        self.eat_token_by_value('while')
        self.eat_token_by_value('(')
        self.complileExpression()
        self.eat_token_by_value(')')
        self.eat_token_by_value('{')
        self.complileStatements()
        self.eat_token_by_value('}')
        self.internal_etree_stack.pop()

    def complileDo(self):
        """Parses a do statement."""
        self.add_sub_element_to_xml('doStatement')
        self.eat_token_by_value('do')
        self.eat_token_by_type(TOKEN_TYPE.IDENTIFIER)
        self.complileSubroutineCall()
        self.eat_token_by_value(';')
        self.internal_etree_stack.pop()

    def complileReturn(self):
        """Parses a return statement."""

        self.add_sub_element_to_xml('returnStatement')
        self.eat_token_by_value('return')

        # 0+ expression
        next_token = self.tokenizer.peek_next_token()
        if next_token.value != ';':
            self.complileExpression()

        self.eat_token_by_value(';')
        self.internal_etree_stack.pop()

    def complileExpressionList(self):
        """Parses an expression list."""

        self.add_sub_element_to_xml('expressionList')

        # 0+ expressions seperated by ','
        expression_count = 0
        while True:
            next_token = self.tokenizer.peek_next_token()

            if (next_token.type not in {TOKEN_TYPE.INTEGER_CONSTANT, TOKEN_TYPE.STRING_CONSTANT, TOKEN_TYPE.IDENTIFIER}
                and next_token.value not in {'true', 'false', 'null', 'this', '(', '-', '~'}
            ):
                break

            self.complileExpression()
            expression_count += 1

            next_token = self.tokenizer.peek_next_token()
            if next_token.value == ',':
                self.eat_token_by_value(',')
            else:
                break

        if expression_count == 0:
            self.insert_xml_empty_escape_string()

        self.internal_etree_stack.pop()

    def complileExpression(self):
        """Parses an expression."""

        self.add_sub_element_to_xml('expression')
        self.compileTerm()

        # 0+ (op term)
        while True:
            next_token = self.tokenizer.peek_next_token()
            if next_token.value not in {'+', '-', '*', '/', '&', '|', '<', '>', '='}:
                break

            self.tokenizer.advance()
            self.add_current_token_to_xml()
            self.compileTerm()

        self.internal_etree_stack.pop()

    def compileTerm(self):
        """Parses a term."""

        self.add_sub_element_to_xml('term')

        next_token = self.tokenizer.peek_next_token()

        if next_token.type == TOKEN_TYPE.INTEGER_CONSTANT:
            self.eat_token_by_type(TOKEN_TYPE.INTEGER_CONSTANT)

        elif next_token.type == TOKEN_TYPE.STRING_CONSTANT:
            self.eat_token_by_type(TOKEN_TYPE.STRING_CONSTANT)

        elif next_token.value in {'true', 'false', 'null', 'this'}:
            self.tokenizer.advance()
            self.add_current_token_to_xml()

        elif next_token.type == TOKEN_TYPE.IDENTIFIER:
            self.eat_token_by_type(TOKEN_TYPE.IDENTIFIER)

            next_token = self.tokenizer.peek_next_token()

            # varName[expression]
            if next_token.value == '[':
                self.eat_token_by_value('[')
                self.complileExpression()
                self.eat_token_by_value(']')

            # subroutineCall
            elif next_token.value in {'(', '.'}:
                self.complileSubroutineCall()

        # (expression)
        elif next_token.value == '(':
            self.eat_token_by_value('(')
            self.complileExpression()
            self.eat_token_by_value(')')

        # unaryOp
        elif next_token.value in {'-', '~'}:
            self.tokenizer.advance()
            self.add_current_token_to_xml()
            self.compileTerm()

        else:
          raise CompilationEngineError(self.tokenizer, f"CompilationEngine.compileTerm() cannot start with '{next_token.value}'")

        self.internal_etree_stack.pop()

    def complileSubroutineCall(self):
        """
        Parses a sub-routine call.

        Assumes the class or sub-routine name has already been eaten.
        """
        next_token = self.tokenizer.peek_next_token()

        # example: 'MyClass.func()'
        if next_token.value == '.':
            self.eat_token_by_value('.')
            self.eat_token_by_type(TOKEN_TYPE.IDENTIFIER)
            self.eat_token_by_value('(')
            self.complileExpressionList()
            self.eat_token_by_value(')')

        # Example: 'func()'
        elif next_token.value == '(':
            self.eat_token_by_value('(')
            self.complileExpressionList()
            self.eat_token_by_value(')')

        else:
            raise CompilationEngineError(self.tokenizer, f"CompilationEngine.complileSubroutineCall() expected '.' or '(' but got '{next_token.value}'")
