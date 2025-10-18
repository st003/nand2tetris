from exceptions import VMTranslatorError

def clean_input_lines(lines: list[str]) -> list[str]:
    """Removes extra whitespace and comment lines."""
    clean_lines: list[str] = []
    for line in lines:
        clean_line = line.strip().lower()
        if (len(clean_line) > 0) and (clean_line[0] != '/'):
            clean_lines.append(clean_line)
    return clean_lines

def is_valid_vm_file(vm_file: str):
    """Checks if the name of the provided vm file is valid."""
    parts = vm_file.split('.')
    if (len(parts) < 2):
        raise VMTranslatorError('Input file is missing file extension')
    if (parts[-1] != 'vm'):
        raise VMTranslatorError('Input file is missing file extension')
