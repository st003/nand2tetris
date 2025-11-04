from constants import ARITHMETIC_LOGICAL_INS_MAP, MEMORY_INS_MAP, MEMORY_SEGMENTS
from exceptions import ParseError

def parse_instruction(line_num, line):
    """Parses the line and returns the associated instruction object."""

    # scrub inline comments
    parts = ''
    inline_comment_index = line.find('//')
    if inline_comment_index != -1:
        line = line[:inline_comment_index].strip()

    parts = line.split(' ')
    parts = parts[:3]

    count = len(parts)

    if count == 1:
        cmd = parts[0].lower()
        if cmd in ARITHMETIC_LOGICAL_INS_MAP:
            return ARITHMETIC_LOGICAL_INS_MAP[cmd](line_num, parts)
        else:
            raise ParseError(f'Invalid vm instruction at line {line_num}:\n\n{line}\n\n"{cmd}" is not a valid arithmetic/logical command.')

    elif count == 2:
        # TODO: implement
        raise ParseError(f'Invalid vm instruction at line {line_num}:\n\n{line}\n\n2-command instructions not support at this time.')

    elif count == 3:
        cmd_0 = parts[0].lower()
        if cmd_0 in MEMORY_INS_MAP:

            cmd_1 = parts[1].lower()
            if cmd_1 not in MEMORY_SEGMENTS:
                raise ParseError(f'Invalid vm instruction at line {line_num}":\n\n{line}\n\n"{cmd_1}" is not a valid memory segment.')

            try:
                cmd_2 = parts[2].lower()
                offset = int(cmd_2)
                if offset < 0:
                    raise ValueError(f'{offset} is less than 0')
            except ValueError:
                raise ParseError(f'Invalid vm instruction at line {line_num}:\n\n{line}\n\n"{cmd_2}" is not a valid offset.')

            return MEMORY_INS_MAP[cmd_0](line_num, parts)
        else:
            raise ParseError(f'Invalid vm instruction at line {line_num}:\n\n{line}\n\n"{cmd_0}" is not a valid memory command.')

    else:
        raise ParseError(f'Invalid vm instruction at line {line_num}:\n\n{line}\n\nIllegal number of commands.')
