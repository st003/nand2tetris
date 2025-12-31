import xml.etree.ElementTree as ET

from exceptions import JackTokenizerError
from lexical_elements import get_token, SYMBOLS
from tokens import StringConstantToken
from xml_formatter import make_pretty

class JackTokenizer():
    """
    Tokenizer for the Jack language.

    Create a single instance of JackTokenizer for each Jack file.
    """

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

    def add_token_to_xml(self):
        """Inserts the current token into the internal XML etree."""
        if self.current_token is not None:
            new_token = ET.SubElement(self.xml_root, self.current_token.type)
            new_token.text = self.current_token.get_xml_value()

    def write_xml(self):
        """Saves the internal XML etree to a file."""
        xml_tree = ET.ElementTree(self.xml_root)
        xml_text = make_pretty(xml_tree, indent=0)
        try:
            with open(self.get_output_file_path(), 'w') as output_file:
                output_file.write(xml_text)
        except Exception as error:
            raise JackTokenizerError(f"Unable to create XML token file at: '{self.get_output_file_path()}'") from error

    def char_is_skippable(self):
        """Determines if the current char can be skipped during tokenization."""

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
        """Determines if the current char terminates a token scan."""

        if self.raw_source_code[self.cursor] in SYMBOLS:
            return True

        if self.char_is_skippable():
            return True

        return False

    def hasMoreTokens(self):
        """Determines if the current Jack file can contain additional tokens."""
        return self.cursor < self.raw_course_code_char_count

    def advance(self):
        """Select the next token in the Jack file."""

        scanning_token = False
        scanning_string_constant = False
        token_start = 0

        while self.hasMoreTokens():

            # start token scan
            if not scanning_token:

                if not self.char_is_skippable():

                    # symbols do not occupy more than a single char
                    if self.raw_source_code[self.cursor] in SYMBOLS:
                        self.current_token = get_token(self.raw_source_code[self.cursor])
                        self.add_token_to_xml()
                        self.cursor += 1
                        break

                    # all other tokens are 2+ characters
                    else:
                        # handle string constants
                        if self.raw_source_code[self.cursor] == '"':
                            scanning_string_constant = True

                        scanning_token = True
                        token_start = self.cursor

            # end token scan
            else:

                # terminate string constants
                if scanning_string_constant and self.raw_source_code[self.cursor] == '"':
                    # strip off the leading and trailing double-quotes
                    string_constant = self.raw_source_code[(token_start + 1):self.cursor]
                    self.current_token = StringConstantToken(string_constant)
                    self.add_token_to_xml()
                    scanning_token = False
                    scanning_string_constant = False
                    self.cursor += 1
                    break

                if not scanning_string_constant and self.char_terminates_token():
                    self.current_token = get_token(self.raw_source_code[token_start:self.cursor])
                    self.add_token_to_xml()
                    scanning_token = False
                    break

            self.cursor += 1

    def tokenType(self):
        """Get the type of the current token."""
        if self.current_token:
            return self.current_token.type
        return None
