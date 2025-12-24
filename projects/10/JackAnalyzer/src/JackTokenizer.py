import uuid

class JackTokenizer():

    def __init__(self, jack_file_path, debug = False):
        self.jack_file_path = jack_file_path
        self.parent_dir = jack_file_path.parent
        self.file_name = jack_file_path.stem
        self.debug = debug

        print(self.get_output_file_name())

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
        # TODO: implement
        pass
