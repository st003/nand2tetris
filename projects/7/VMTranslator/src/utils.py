from pathlib import Path

from exceptions import VMTranslatorError

def get_vm_file_name(vm_file_path: str) -> str:
    """
    Checks if the name of the provided vm file is valid and returns
    the file name sans directories.
    """
    path = Path(vm_file_path)

    if (not path.suffix):
        raise VMTranslatorError('Input file is missing file extension')
    if (path.suffix != '.vm'):
        raise VMTranslatorError(f'{path.suffix} is an invalid file extension')

    return path.stem
