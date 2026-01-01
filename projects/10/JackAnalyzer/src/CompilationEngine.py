import xml.etree.ElementTree as ET

from exceptions import CompilationEngineError
from JackTokenizer import JackTokenizer
from xml_formatter import make_pretty

class CompilationEngine():
    """Class for lexing and parsing Jack source code."""

    def __init__(self, jack_file_path, debug = False):
        self.jack_file_path = jack_file_path
        self.parent_dir = jack_file_path.parent
        self.file_name = jack_file_path.stem
        self.debug = debug
        self.xml_root = ET.Element('class')

    def get_output_file_path(self):
        if self.debug:
            return f'{self.parent_dir}/{self.file_name}_DEBUG.xml'
        return f'{self.parent_dir}/{self.file_name}.xml'

    def add_token_to_xml(self, token):
        """Inserts the current token into the internal XML etree."""
        if token is not None:
            new_token = ET.SubElement(self.xml_root, token.type)
            new_token.text = token.get_xml_value()

    def write_xml(self):
        """Saves the internal XML etree to a file."""
        xml_tree = ET.ElementTree(self.xml_root)
        xml_text = make_pretty(xml_tree, indent=2)
        try:
            with open(self.get_output_file_path(), 'w') as output_file:
                output_file.write(xml_text)
        except Exception as error:
            raise CompilationEngineError(f"Unable to create XML class file at: '{self.get_output_file_path()}'") from error

    def compileClass(self):
        tokenizer = JackTokenizer(self.jack_file_path, self.debug)
        while tokenizer.hasMoreTokens():
            tokenizer.advance()
            self.add_token_to_xml(tokenizer.current_token)
        tokenizer.write_xml()
        self.write_xml()

    # TODO: definitions found at:
    # 4.5
    # 4.8 @12:50+

    def complileClassVarDec(self):
        """."""
        # TODO: implement
        pass

    def complileSubroutineDec(self):
        """."""
        # TODO: implement
        pass

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
