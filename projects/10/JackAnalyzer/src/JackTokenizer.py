import xml.etree.ElementTree as ET

from exceptions import JackTokenizerError

class JackTokenizer():

    def __init__(self, jack_file_path, debug = False):

        self.parent_dir = jack_file_path.parent
        self.file_name = jack_file_path.stem
        self.debug = debug

        self.cursor = 0
        self.current_token = None

        self.xml_root = ET.Element('tokens')

        with open(jack_file_path, 'r', encoding='utf-8') as jack_file:
            self.raw_source_code = jack_file.read()
            self.raw_course_code_char_count = len(self.raw_source_code)

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

    def char_is_skippable(self):
        return self.raw_source_code[self.cursor].isspace()

    def char_terminates_token(self):
        return self.char_is_skippable()

    def hasMoreTokens(self):
        return self.cursor < self.raw_course_code_char_count

    def advance(self):

        scanning_token = False
        token_start = 0

        while self.hasMoreTokens():

            if not scanning_token:

                # start token scan
                if not self.char_is_skippable():
                    scanning_token = True
                    token_start = self.cursor

            else:

                # complete token scan
                if self.char_terminates_token():
                    self.current_token = self.raw_source_code[token_start:self.cursor]

                    new_token = ET.SubElement(self.xml_root, 'token')
                    new_token.text = self.current_token
                    new_token.tail = '\n' # TODO: investigate alternatives to pretty-printing

                    scanning_token = False
                    # exit loop so only a single token is captured
                    break

            self.cursor += 1

    def tokenType(self):
        # TODO: implement
        pass
