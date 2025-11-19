from pathlib import Path

from exceptions import VMTranslatorError

class Line():
    """Class for containing a line and its meta-data."""
    def __init__(self, file_name, raw_line):
        self.file_name = file_name
        self.raw_line = raw_line.strip()
        self.line_num = 0
        self.tokens = None

    def is_empty(self):
        """Indicates if a line is empty."""
        return len(self.raw_line) == 0

    def is_comment(self):
        """Indicates if a line contains only a comment."""
        return self.raw_line[0] == '/'

    def __str__(self):
        return self.raw_line

def get_input_lines(paths):
    """
    Opens all files specified in a list and loads
    their contents into a list of Line objects
    """
    file_count = len(paths)
    input_lines = []
    for path in paths:
        with open(path, 'r') as vm_file:
            for line in vm_file.readlines():
                input_lines.append(Line(path.stem, line))
    return input_lines, file_count

def get_vm_files(path):
    """
    Evaluates a file or directory and returns:

    1. A list of paths to vm files
    2. The path string to the future ASM output file
    """

    path = Path(path)

    vm_files = []

    if (path.is_dir()):
        for file in path.iterdir():
            if file.suffix == '.vm':
                vm_files.append(file)

    else:
        if (not path.suffix):
            raise VMTranslatorError('Input file is missing file extension')
        if (path.suffix != '.vm'):
            raise VMTranslatorError(f'{path.suffix} is an invalid file extension')

        vm_files.append(path)

    output_file_path = f'{path.parent}/{path.stem}.asm'

    return vm_files, output_file_path
