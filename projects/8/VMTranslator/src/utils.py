from pathlib import Path

from exceptions import VMTranslatorError

def get_vm_file_name(vm_file_path):
    """
    Checks if the name of the provided vm file is valid and returns
    the parent directory Path and file name sans extension.
    """
    path = Path(vm_file_path)

    if (not path.suffix):
        raise VMTranslatorError('Input file is missing file extension')
    if (path.suffix != '.vm'):
        raise VMTranslatorError(f'{path.suffix} is an invalid file extension')

    return path.parent, path.stem
