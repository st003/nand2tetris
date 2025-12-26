import uuid

class JackTokenizer():

    def __init__(self, jack_file_path, debug = False):

        self.parent_dir = jack_file_path.parent
        self.file_name = jack_file_path.stem
        self.debug = debug

        self.current_token = None
        self.token_type = None

        with open(jack_file_path, 'r', encoding='utf-8') as jack_file:
            self.raw_source_code = jack_file.read()

    def get_output_file_name(self):
        if self.debug:
            new_uuid = uuid.uuid4()
            return f'{self.parent_dir}/{self.file_name}T_{str(new_uuid)[:8]}.xml'
        return f'{self.parent_dir}/{self.file_name}T.xml'

    def hasMoreTokens():
        # TODO: implement
        return False

    def advance():
        # TODO: implement
        pass

    def tokenType():
        return self.token_type
