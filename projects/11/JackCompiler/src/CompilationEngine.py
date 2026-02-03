import xml.etree.ElementTree as ET

from constants import IDENTIFER_ATTR, TOKEN_TYPE
from exceptions import CompilationEngineError, SymbolTableError
from JackTokenizer import JackTokenizer
from xml_formatter import make_pretty
from SymbolTable import SymbolTable
from VMWriter import VMWriter

class CompilationEngine():
    """Class for lexing and parsing Jack source code."""

    def __init__(self, jack_file_path, verbose=False):

        self.parent_dir = jack_file_path.parent
        self.file_name = jack_file_path.stem
        self.verbose_output = verbose

        self.tokenizer = JackTokenizer(jack_file_path)
        self.symbol_table = SymbolTable()
        self.class_name = None
        self.current_subroutine = None
        self.current_subroutine_type = None

        self.vm_writer = VMWriter(f'{self.parent_dir}/{self.file_name}')

        # store the etree as a stack so the final xml is not flat
        self.internal_etree_stack = [ET.Element('class')]

    def get_current_subroutine_full_name(self):
        """Constucts the current subroutine name using the 'Class.subroutine' format."""
        return f'{self.file_name}.{self.current_subroutine}'

    def write_vm_file(self):
        """Writes the VM file output."""
        self.vm_writer.close()

    def get_xml_output_file_path(self):
        """Returns the output file path for the XML file."""
        return f'{self.parent_dir}/{self.file_name}.xml'

    def add_current_token_to_xml(self, attrs=None):
        """
        Inserts the current token into the internal XML etree.

        Optionally define custom attributes for XML tag.
        """
        if self.tokenizer.current_token is not None:
            # always use the top of the stack
            new_token = ET.SubElement(self.internal_etree_stack[-1], self.tokenizer.current_token.type)
            new_token.text = self.tokenizer.current_token.get_xml_value()
            if attrs is not None:
                for k, v in attrs.items():
                    new_token.set(k, str(v))

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
            with open(self.get_xml_output_file_path(), 'w') as output_file:
                output_file.write(xml_text)
        except OSError as error:
            raise IOError(f"Unable to create XML class file at: '{self.get_xml_output_file_path()}'") from error

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

    def eat_symbol_token(self, defined_or_used, symbol_type=None, symbol_kind=None):
        """Advances to the next identifier token and updates the symbol table."""
        self.tokenizer.advance()

        if self.tokenizer.tokenType() != TOKEN_TYPE.IDENTIFIER:
            raise CompilationEngineError(self.tokenizer, f'CompilationEngine.eat_symbol_token() expected token but got is not an identifier')

        name = self.get_current_token_value()
        if defined_or_used == IDENTIFER_ATTR.DEFINED:
            self.symbol_table.define(name, symbol_type, symbol_kind)

        # add identifier attributes
        try:
            category = symbol_kind if symbol_kind else self.symbol_table.KindOf(name)
            attrs = {'category': category, 'index': self.symbol_table.IndexOf(name)}
            attrs[defined_or_used] = 'true'
            self.add_current_token_to_xml(attrs=attrs)
        except SymbolTableError:
            # skip XML attributes when you cannot locate a symbol
            self.add_current_token_to_xml()

    def token_is_type(self, token):
        """Check if the current token is valid return type."""
        # NOTE: technically 'identifier' is not enough to prove it's a class definition
        return (token.value in {'int', 'char', 'boolean'}
                or token.type == TOKEN_TYPE.IDENTIFIER)

    def compileClass(self):
        """Parses a class declaration."""

        self.vm_writer.writeComment(f'Compiled {self.file_name}.jack:')
        self.eat_token_by_value('class')

        # capture the class name for definine 'this' in method argument
        self.eat_token_by_type(TOKEN_TYPE.IDENTIFIER)
        self.class_name = self.get_current_token_value()

        self.eat_token_by_value('{')

        while True:
            if self.compileClassVarDec():
                continue
            break

        if self.verbose_output:
            self.symbol_table.print_class_table(self.file_name)

        while True:
            if self.complileSubroutineDec():
                continue
            break

        self.eat_token_by_value('}')

    def compileClassVarDec(self):
        """Parses a class variable declaration."""

        next_token = self.tokenizer.peek_next_token()
        if next_token.value not in {'static', 'field'}:
            return False

        self.add_sub_element_to_xml('classVarDec')

        self.tokenizer.advance()
        symbol_kind = self.get_current_token_value()
        self.add_current_token_to_xml()

        # type
        symbol_type = None
        next_token = self.tokenizer.peek_next_token()
        if self.token_is_type(next_token):
            self.tokenizer.advance()
            symbol_type = self.get_current_token_value()
            self.add_current_token_to_xml()
        else:
            raise CompilationEngineError(self.tokenizer, f"'{next_token.value}' is not a valid type")

        # 1+ variable names separated by ','
        self.eat_symbol_token(IDENTIFER_ATTR.DEFINED, symbol_type, symbol_kind)
        while True:
            next_token = self.tokenizer.peek_next_token()
            if next_token.value != ',':
                break
            self.eat_token_by_value(',')
            self.eat_symbol_token(IDENTIFER_ATTR.DEFINED, symbol_type, symbol_kind)

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
        self.current_subroutine_type = self.get_current_token_value()
        self.add_current_token_to_xml()

        self.symbol_table.startSubroutine()

        # for methods, insert the 'this' as the first argument
        if self.current_subroutine_type == 'method':
            self.symbol_table.define('this', self.class_name, 'argument')

        # return type
        next_token = self.tokenizer.peek_next_token()
        if next_token.value == 'void' or self.token_is_type(next_token):
            self.tokenizer.advance()
            self.add_current_token_to_xml()
        else:
            raise CompilationEngineError(self.tokenizer, f"{next_token.value} is not a valid sub-routine return type")

        # function name
        self.eat_token_by_type(TOKEN_TYPE.IDENTIFIER)
        self.current_subroutine = self.get_current_token_value()

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

            symbol_type = self.get_current_token_value()
            symbol_kind = 'argument'

            self.eat_symbol_token(IDENTIFER_ATTR.DEFINED, symbol_type, symbol_kind)

            while True:
                next_token = self.tokenizer.peek_next_token()
                if next_token.value != ',':
                    break

                self.eat_token_by_value(',')

                self.tokenizer.advance() # this is the type
                self.add_current_token_to_xml()
                symbol_type = self.get_current_token_value()

                self.eat_symbol_token(IDENTIFER_ATTR.DEFINED, symbol_type, symbol_kind)

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

        if self.verbose_output:
            self.symbol_table.print_subroutine_table(self.current_subroutine_type, self.current_subroutine)

        self.vm_writer.writeFunction(self.get_current_subroutine_full_name(), self.symbol_table.VarCount('local'))

        # for constructor, before any statements are parsed, you need to get the number of class-fields,
        # allocate memory for the object, and then place the new object's pointer into 'this'
        if self.current_subroutine_type == 'constructor':
            self.vm_writer.writePush('constant', self.symbol_table.VarCount('field'))
            self.vm_writer.writeCall('Memory.alloc', 1)
            self.vm_writer.writePop('pointer', 0)

        # for methods, before any statements are parsed, put the first argument (this) into the
        # this memory segment
        if self.current_subroutine_type == 'method':
            self.vm_writer.writePush('argument', 0)
            self.vm_writer.writePop('pointer', 0)

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

        symbol_kind = 'local'
        symbol_type = None

        next_token = self.tokenizer.peek_next_token()
        if self.token_is_type(next_token):
            self.tokenizer.advance()
            self.add_current_token_to_xml()
            symbol_type = self.get_current_token_value()
        else:
            raise CompilationEngineError(self.tokenizer, f"{next_token.value} is not a valid type")

        # get 1 or more variable names
        self.eat_symbol_token(IDENTIFER_ATTR.DEFINED, symbol_type, symbol_kind)
        while True:
            next_token = self.tokenizer.peek_next_token()
            if next_token.value == ',':
                self.eat_token_by_value(',')
                self.eat_symbol_token(IDENTIFER_ATTR.DEFINED, symbol_type, symbol_kind)
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
        setting_array = False

        self.add_sub_element_to_xml('letStatement')
        self.eat_token_by_value('let')

        # variable name
        self.eat_symbol_token(IDENTIFER_ATTR.USED)
        var_name = self.get_current_token_value()

        next_token = self.tokenizer.peek_next_token()

        # set position in array
        if next_token.value == '[':
            setting_array = True
            self.eat_token_by_value('[')
            self.complileExpression()
            self.eat_token_by_value(']')
            self.eat_token_by_value('=')

            # calculate array position by adding the array base address
            # to the index offset value
            self.vm_writer.writePush(self.symbol_table.KindOf(var_name), self.symbol_table.IndexOf(var_name))
            self.vm_writer.WriteArithmatic('+')

        # set variable
        elif next_token.value == '=':
            self.eat_token_by_value('=')

        else:
            raise CompilationEngineError(self.tokenizer, f"CompilationEngine.complileLet() expected '[' or '=' but got '{next_token.value}'")

        self.complileExpression()
        self.eat_token_by_value(';')

        if setting_array:
            self.vm_writer.writePop('temp', 0) # backup of the value to be set (from the expression)
            self.vm_writer.writePop('pointer', 1) # select 'that' (the array pointer)
            self.vm_writer.writePush('temp', 0) # return the value to be set to the stack
            self.vm_writer.writePop('that', 0) # set the value into the head of the array
        else:
            # when setting a non-array variable, pop the value into the memory segement
            self.vm_writer.writePop(self.symbol_table.KindOf(var_name), self.symbol_table.IndexOf(var_name))

        self.internal_etree_stack.pop()

    def complileIf(self):
        """Parses an if statement."""

        self.add_sub_element_to_xml('ifStatement')
        self.eat_token_by_value('if')
        self.eat_token_by_value('(')
        self.complileExpression()
        self.eat_token_by_value(')')

        # generate a label for exiting the if condition
        exit_label = f'{self.class_name}_{self.vm_writer.label_count}'
        self.vm_writer.increment_label_count()
        # generate a label for jumping to the else condition
        else_label = f'{self.class_name}_{self.vm_writer.label_count}'
        self.vm_writer.increment_label_count()

        self.vm_writer.WriteIf(else_label)

        self.eat_token_by_value('{')
        self.complileStatements()
        self.eat_token_by_value('}')

        # at the end of the if condition, goto the exit label
        self.vm_writer.WriteGoto(exit_label)
        # always place the else label, even if there is no else condition
        self.vm_writer.WriteLabel(else_label)

        # 0+ else
        next_token = self.tokenizer.peek_next_token()
        if next_token.value == 'else':
            self.eat_token_by_value('else')
            self.eat_token_by_value('{')
            self.complileStatements()
            self.eat_token_by_value('}')

        self.vm_writer.WriteLabel(exit_label)

        self.internal_etree_stack.pop()

    def complileWhile(self):
        """Parses a while statement."""
        self.add_sub_element_to_xml('whileStatement')

        # generate a label for the beginning of the while loop
        start_label = f'{self.class_name}_{self.vm_writer.label_count}'
        self.vm_writer.WriteLabel(start_label)
        self.vm_writer.increment_label_count()

        self.eat_token_by_value('while')
        self.eat_token_by_value('(')

        self.complileExpression()

        # generate a label for the end of the while loop
        end_label = f'{self.class_name}_{self.vm_writer.label_count}'
        self.vm_writer.WriteIf(end_label)
        self.vm_writer.increment_label_count()

        self.eat_token_by_value(')')
        self.eat_token_by_value('{')
        self.complileStatements()
        self.eat_token_by_value('}')

        self.internal_etree_stack.pop()
        self.vm_writer.WriteGoto(start_label)
        self.vm_writer.WriteLabel(end_label)

    def complileDo(self):
        """Parses a do statement."""
        self.add_sub_element_to_xml('doStatement')
        self.eat_token_by_value('do')
        self.eat_token_by_type(TOKEN_TYPE.IDENTIFIER)

        # determine if called class/subroutine is for a method by
        # checking if it was declared in the symbol table
        # TODO: does this work for func() type calls?
        class_or_func_name = self.get_current_token_value()
        is_method = self.symbol_table.varExists(class_or_func_name)
        self.complileSubroutineCall(is_method=is_method)

        self.eat_token_by_value(';')

        # TODO: should this always happen? or only when the function return is 'void'?
        self.vm_writer.writePop('temp', 0)
        self.internal_etree_stack.pop()

    def complileReturn(self):
        """Parses a return statement."""

        self.add_sub_element_to_xml('returnStatement')
        self.eat_token_by_value('return')

        # 0+ expression
        next_token = self.tokenizer.peek_next_token()
        if next_token.value != ';':
            self.complileExpression()
        else:
            # when *not* returning a value, always return 0
            self.vm_writer.writePush('constant', 0)

        self.eat_token_by_value(';')

        self.vm_writer.writeReturn()
        self.internal_etree_stack.pop()

    def complileExpressionList(self):
        """Parses an expression list and returns the number of expressions."""

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
        return expression_count

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
            op = self.get_current_token_value()
            self.add_current_token_to_xml()
            self.compileTerm()

            self.vm_writer.WriteArithmatic(op)

        self.internal_etree_stack.pop()

    def compileTerm(self):
        """Parses a term."""

        self.add_sub_element_to_xml('term')

        next_token = self.tokenizer.peek_next_token()

        if next_token.type == TOKEN_TYPE.INTEGER_CONSTANT:
            self.eat_token_by_type(TOKEN_TYPE.INTEGER_CONSTANT)
            self.vm_writer.writePush('constant', self.get_current_token_value())

        elif next_token.type == TOKEN_TYPE.STRING_CONSTANT:
            self.eat_token_by_type(TOKEN_TYPE.STRING_CONSTANT)
            self.vm_writer.writeStringConstant(self.get_current_token_value())

        elif next_token.value in {'true', 'false', 'null', 'this'}:
            self.tokenizer.advance()
            self.add_current_token_to_xml()
            self.vm_writer.writeKeyword(self.get_current_token_value())

        elif next_token.type == TOKEN_TYPE.IDENTIFIER:
            self.eat_symbol_token(IDENTIFER_ATTR.USED)

            next_token = self.tokenizer.peek_next_token()

            # varName[expression]
            if next_token.value == '[':
                array_var = self.get_current_token_value()

                self.eat_token_by_value('[')
                self.complileExpression()
                self.eat_token_by_value(']')

                # calculate array position by adding the array base address to the index offset value
                self.vm_writer.writePush(self.symbol_table.KindOf(array_var), self.symbol_table.IndexOf(array_var))
                self.vm_writer.WriteArithmatic('+')

                # then select the array pointer and push the value in the array onto the stack
                self.vm_writer.writePop('pointer', 1)
                self.vm_writer.writePush('that', 0)

            # subroutineCall
            elif next_token.value in {'(', '.'}:
                self.complileSubroutineCall()

            # identifier must be a variable that is being passed in to
            # a function as an argument
            else:
                var_name = self.get_current_token_value()
                self.vm_writer.writePush(self.symbol_table.KindOf(var_name), self.symbol_table.IndexOf(var_name))

        # (expression)
        elif next_token.value == '(':
            self.eat_token_by_value('(')
            self.complileExpression()
            self.eat_token_by_value(')')

        # unaryOp
        elif next_token.value in {'-', '~'}:
            self.tokenizer.advance()
            unary_op = self.get_current_token_value()
            self.add_current_token_to_xml()
            self.compileTerm()
            self.vm_writer.writeUnaryOp(unary_op)

        else:
          raise CompilationEngineError(self.tokenizer, f"CompilationEngine.compileTerm() cannot start with '{next_token.value}'")

        self.internal_etree_stack.pop()

    def complileSubroutineCall(self, is_method=False):
        """
        Parses a sub-routine call.

        Assumes the class or sub-routine name has already been eaten.
        """
        class_or_func_name = self.get_current_token_value()

        next_token = self.tokenizer.peek_next_token()

        # example: 'MyClass.func()'
        if next_token.value == '.':

            # class methods require the class instance be pushed onto the stack
            # so it can be used as the first argument
            if is_method:
                self.vm_writer.writePush(self.symbol_table.KindOf(class_or_func_name), self.symbol_table.IndexOf(class_or_func_name))

            self.eat_token_by_value('.')
            self.eat_token_by_type(TOKEN_TYPE.IDENTIFIER)
            func_name = self.get_current_token_value()

            self.eat_token_by_value('(')
            n_args = self.complileExpressionList()
            self.eat_token_by_value(')')

            # for class methods:
            # (1) the vm function call uses the class name, no the variable name
            # (2) 'this' argument does not appear in the expression list count
            if is_method:
                class_or_func_name = self.symbol_table.TypeOf(class_or_func_name)
                n_args += 1

            self.vm_writer.writeCall(f'{class_or_func_name}.{func_name}', n_args)

        # Example: 'func()'
        elif next_token.value == '(':
            self.eat_token_by_value('(')
            n_args = self.complileExpressionList()
            self.eat_token_by_value(')')

            # stand-alone function calls are always method calls
            func_name = class_or_func_name
            class_or_func_name = self.class_name
            # 'this' argument does not appear in the expression list count
            n_args += 1
            # because we can only use this format inside a class method, the 'this' pointer
            # must already be selected and is the first argument
            self.vm_writer.writePush('pointer', 0)
            self.vm_writer.writeCall(f'{class_or_func_name}.{func_name}', n_args)

        else:
            raise CompilationEngineError(self.tokenizer, f"CompilationEngine.complileSubroutineCall() expected '.' or '(' but got '{next_token.value}'")
