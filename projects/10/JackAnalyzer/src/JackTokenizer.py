import xml.etree.ElementTree as ET

from exceptions import JackTokenizerError

class JackTokenizer():

    def __init__(self, jack_file_path, debug = False):

        self.parent_dir = jack_file_path.parent
        self.file_name = jack_file_path.stem
        self.debug = debug

        self.cursor = 0
        self.current_token = None
        self.is_single_line_comment = False
        self.is_multi_line_comment = False

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

        # check for comment start
        if (not self.is_single_line_comment
            and not self.is_multi_line_comment
            and self.cursor < (self.raw_course_code_char_count - 2)
        ):
            potential_comment = self.raw_source_code[self.cursor:(self.cursor + 2)]
            if potential_comment == '//':
                self.is_single_line_comment = True
            elif potential_comment == '/*':
                self.is_multi_line_comment = True

        # check for comment end
        if self.is_single_line_comment:
            if self.raw_source_code[self.cursor] == '\n':
                self.is_single_line_comment = False

        elif self.is_multi_line_comment and self.cursor < (self.raw_course_code_char_count - 2):
            if self.raw_source_code[self.cursor:(self.cursor + 2)] == '*/':
                self.is_multi_line_comment = False
                self.cursor += 2

        if self.is_single_line_comment or self.is_multi_line_comment:
            return True

        if self.raw_source_code[self.cursor].isspace():
            return True

        return False

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
                    new_token.text = f' {self.current_token} '
                    new_token.tail = '\n' # TODO: investigate alternatives to pretty-printing?

                    scanning_token = False
                    # exit loop so only a single token is captured
                    break

            self.cursor += 1

    def tokenType(self):
        # TODO: implement
        pass
