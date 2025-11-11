from pathlib import Path

from exceptions import VMTranslatorError

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
