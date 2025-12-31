from JackTokenizer import JackTokenizer

class CompilationEngine():
    """Class for lexing and parsing Jack source code."""

    def __init__(self, jack_file_path, debug = False):
        self.jack_file_path = jack_file_path
        self.parent_dir = jack_file_path.parent
        self.file_name = jack_file_path.stem
        self.debug = debug

    def get_output_file_name(self):
        if self.debug:
            return f'{self.parent_dir}/{self.file_name}_DEBUG.xml'
        return f'{self.parent_dir}/{self.file_name}.xml'

    def compile(self):
        tokenizer = JackTokenizer(self.jack_file_path, self.debug)
        while tokenizer.hasMoreTokens():
            tokenizer.advance()
        tokenizer.write_xml()
