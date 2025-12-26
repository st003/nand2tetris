import xml.etree.ElementTree as ET

from exceptions import JackTokenizerError

class JackTokenizer():

    def __init__(self, jack_file_path, debug = False):

        self.parent_dir = jack_file_path.parent
        self.file_name = jack_file_path.stem
        self.debug = debug

        self.current_token = None
        self.token_type = None

        self.xml_root = ET.Element('tokens')

        with open(jack_file_path, 'r', encoding='utf-8') as jack_file:
            self.raw_source_code = jack_file.read()

    def get_output_file_path(self):
        if self.debug:
            return f'{self.parent_dir}/{self.file_name}T_DEBUG.xml'
        return f'{self.parent_dir}/{self.file_name}T.xml'

    def write_xml(self):
        xml_tree = ET.ElementTree(self.xml_root)
        try:
            with open(self.get_output_file_path(), 'wb') as output_file:
                xml_tree.write(output_file, encoding='utf-8')
        except IOError as error:
            raise JackTokenizerError(f"Unable to create XML token file at: '{self.get_output_file_path()}'") from error

    def hasMoreTokens():
        # TODO: implement
        return False

    def advance():
        # TODO: implement
        pass

    def tokenType():
        return self.token_type
