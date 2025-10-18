from exceptions import VMTranslatorError

def is_valid_vm_file(vm_file: str):
    """Checks if the name of the provided vm file is valid."""

    parts = vm_file.split('.')

    if (len(parts) != 2):
        raise VMTranslatorError('Input file is missing file extension')

    if (parts[1] != 'vm'):
        raise VMTranslatorError('Input file is missing file extension')

