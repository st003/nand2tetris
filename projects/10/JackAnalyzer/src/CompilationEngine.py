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

    def add_token_to_xml(self, token):
        """Inserts the token into the internal XML etree."""
        if token is not None:
            # always use the top of the stack
            new_token = ET.SubElement(self.internal_etree_stack[-1], token.type)
            new_token.text = token.get_xml_value()

    def add_current_token_to_xml(self):
        """Inserts the current token into the internal XML etree."""
        self.add_token_to_xml(self.tokenizer.current_token)

    def add_sub_element_to_xml(self, name):
        """Creates a new sub-element in the xml and move it to the top of the etree stack."""
        if name is not None:
            new_sub_element = ET.SubElement(self.internal_etree_stack[-1], name)
            # push onto the stack so subsequent elements are nested
            self.internal_etree_stack.append(new_sub_element)

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

    def current_token_in(self, set):
        """Checks the current token's value membership against a provided set."""
        return (self.get_current_token_value() in set)

    def token_is_return_type(self):
        """Check if the current token is valid return type."""
        # NOTE: technically 'identifier' is not enough to prove it's a class definition
        return (self.get_current_token_value() in {'int', 'char', 'boolean'}
                or self.tokenizer.tokenType() == TOKEN_TYPE.IDENTIFIER)

    # TODO: definitions found at:
    # 4.5 @2:19
    # 4.8 @12:50+

    def compileClass(self):
        """Parses a class declaration."""
        self.eat_token_by_value('class')
        self.eat_token_by_type(TOKEN_TYPE.IDENTIFIER)
        self.eat_token_by_value('{')

        while True:
            self.tokenizer.advance()
            if self.complileClassVarDec() or self.complileSubroutineDec():
                continue
            else:
                # TODO: check for and add '}'
                break

    def complileClassVarDec(self):
        """."""
        # TODO: implement
        return False

    def complileSubroutineDec(self):
        """Parses a sub-routine declaration."""
        if not self.current_token_in({'constructor', 'function', 'method'}):
            return False

        self.add_sub_element_to_xml('subroutineDec')
        self.add_current_token_to_xml()

        self.tokenizer.advance()
        if self.get_current_token_value() == 'void' or self.token_is_return_type():
            self.add_current_token_to_xml()
        else:
            raise CompilationEngineError(self.tokenizer, f"{self.get_current_token_value()} is not a valid sub-routine return type")

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
        # TODO: implement parameter list args
        self.internal_etree_stack.pop()

    def complileSubroutineBody(self):
        """Parses a sub-routine body."""

        self.add_sub_element_to_xml('subroutineBody')
        self.eat_token_by_value('{')

        # variable declarations
        while True:
            self.tokenizer.advance()
            if self.complileVarDec():
                continue
            else:
                break

        # statements
        self.complileStatements()

        # TODO: uncomment when complileStatements() is complete
        # if self.get_current_token_value() == '}':
        #     self.add_current_token_to_xml()
        # else:
        #     raise CompilationEngineError(self.tokenizer, "Expected '}' but got '" + f"{self.get_current_token_value()}'")

        self.internal_etree_stack.pop()

    def complileVarDec(self):
        """Parses a var declaration. Evaluates the current token."""

        if not self.current_token_in({'var'}):
            return False

        self.add_sub_element_to_xml('varDec')
        self.add_current_token_to_xml()

        self.tokenizer.advance()
        if self.token_is_return_type():
            self.add_current_token_to_xml()
        else:
            raise CompilationEngineError(self.tokenizer, f"{self.get_current_token_value()} is not a valid return type")

        # get 1 or more variable names
        self.eat_token_by_type(TOKEN_TYPE.IDENTIFIER)
        while True:
            self.tokenizer.advance()
            if self.get_current_token_value() == ',':
                self.add_current_token_to_xml()
                self.eat_token_by_type(TOKEN_TYPE.IDENTIFIER)
            elif self.get_current_token_value() == ';':
                self.add_current_token_to_xml()
                break
            else:
                raise CompilationEngineError(self.tokenizer, f"Expected ',' or ';' not '{self.get_current_token_value()}'")

        self.internal_etree_stack.pop()
        return True

    def complileStatements(self):
        """Parses all statements by type. Evaluates the current token."""

        if not self.current_token_in({'let', 'if', 'while', 'do', 'return'}):
            return

        self.add_sub_element_to_xml('statements')

        while True:

            if not self.current_token_in({'let', 'if', 'while', 'do', 'return'}):
                break

            stmnt = self.get_current_token_value()
            if stmnt == 'let':
                self.complileLet()
            elif stmnt == 'if':
                pass
            elif stmnt == 'while':
                pass
            elif stmnt == 'do':
                pass
            elif stmnt == 'return':
                pass

            self.tokenizer.advance()

        self.internal_etree_stack.pop()

    def complileLet(self):
        """Parses a let statement."""

        self.add_sub_element_to_xml('letStatement')
        self.add_current_token_to_xml() # expect the current token to be 'let'
        self.eat_token_by_type(TOKEN_TYPE.IDENTIFIER)

        self.tokenizer.advance()
        if self.get_current_token_value() == '[':
            self.complileExpression()
            self.eat_token_by_value(']')
            self.eat_token_by_value('=')

        elif self.get_current_token_value() == '=':
            self.add_current_token_to_xml()

        else:
            raise CompilationEngineError(self.tokenizer, f"let statement expected '[' or '=' but found {self.get_current_token_value()}")

        self.tokenizer.advance()
        self.complileExpression()
        self.eat_token_by_value(';')

        self.internal_etree_stack.pop()

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
        """Parses an expression."""
        self.add_sub_element_to_xml('expression')

        self.complileTerm()
        # TODO: 1+ (op term)

        self.internal_etree_stack.pop()

    def complileTerm(self):
        """Parses a term."""

        self.add_sub_element_to_xml('term')

        if self.tokenizer.tokenType() == TOKEN_TYPE.INTEGER_CONSTANT:
            self.add_current_token_to_xml()

        elif self.tokenizer.tokenType() == TOKEN_TYPE.STRING_CONSTANT:
            self.add_current_token_to_xml()

        elif self.current_token_in({'true', 'false', 'null', 'this'}):
            self.add_current_token_to_xml()

        elif self.tokenizer.tokenType() == TOKEN_TYPE.IDENTIFIER:
            previous_token = self.tokenizer.current_token
            self.tokenizer.advance()

            # function subroutineCall
            if self.get_current_token_value() == '.':
                self.add_token_to_xml(previous_token)
                self.add_current_token_to_xml() # this is the '.'
                self.eat_token_by_type(TOKEN_TYPE.IDENTIFIER)
                self.eat_token_by_value('(')
                self.complileExpressionList()

                if self.get_current_token_value() == ')':
                    self.add_current_token_to_xml()
                else:
                    self.eat_token_by_value(')')

            # TODO: method subroutineCall
            elif self.get_current_token_value() == '(':
                pass

            # TODO: varName[expression]
            elif self.get_current_token_value() == '[':
                pass

            # varName
            else:
                self.add_token_to_xml(previous_token)

        # TODO: (expression)

        elif self.current_token_in({'-', '~'}):
            self.add_current_token_to_xml()
            self.tokenizer.advance()
            self.complileTerm()
        else:
          # TODO: throw and error here?
          pass

        self.internal_etree_stack.pop()

    def complileExpressionList(self):
        """Parses an expression list."""
        self.add_sub_element_to_xml('expressionList')
        self.tokenizer.advance()
        # TODO: 0+ expressions sperated by ','
        self.complileExpression()
        self.internal_etree_stack.pop()

