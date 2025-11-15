from constants import ARITHMETIC_LOGICAL_INS_MAP, BRANCH_INS_MAP, FUNCTION_INS_MAP, MEMORY_INS_MAP, MEMORY_SEGMENTS
from exceptions import ParseError

def tokenize(raw_line):
    """Parse raw line in a list of tokens."""
    tokens = raw_line.split(' ')

    try:
        comment_index = tokens.index('//')
        tokens = tokens[:comment_index]
    except:
        pass

    tokens = [t for t in tokens if t != '']
    return tokens

def check_offset(line_num, line, cmd_2):
    """Checks that an offset meets implementation requirements."""
    try:
        offset = int(cmd_2.lower())
        if offset < 0:
            raise ValueError(f'{offset} is less than 0')
    except ValueError:
        raise ParseError(f'Invalid vm instruction at line {line_num}:\n\n{line}\n\n"{cmd_2}" is not a valid offset.')

def parse_instruction(line):
    """Parses the line and returns the associated instruction object."""

    line.tokens = tokenize(line.raw_line)
    token_count = len(line.tokens)

    # arithmetic/logical commands + function returns
    if token_count == 1:
        cmd = line.tokens[0].lower()
        if cmd in ARITHMETIC_LOGICAL_INS_MAP:
            return ARITHMETIC_LOGICAL_INS_MAP[cmd](line.line_num, line.tokens)

        elif cmd in FUNCTION_INS_MAP:
            return FUNCTION_INS_MAP[cmd](line.line_num, line.tokens)

        else:
            raise ParseError(f'Invalid vm instruction at line {line.line_num}:\n\n{line}\n\n"{cmd}" is not a valid arithmetic/logical command.')

    # branching commands
    elif token_count == 2:
        cmd_0 = line.tokens[0]
        if cmd_0 not in BRANCH_INS_MAP:
            raise ParseError(f'Invalid vm instruction at line {line.line_num}:\n\n{line}\n\n"{cmd_0}" is not a valid branching command.')

        return BRANCH_INS_MAP[cmd_0](line.line_num, line.tokens)

    # memory commands + function declarations / calls
    elif token_count == 3:
        cmd_0 = line.tokens[0].lower()
        if cmd_0 in MEMORY_INS_MAP:

            cmd_1 = line.tokens[1].lower()
            if cmd_1 not in MEMORY_SEGMENTS:
                raise ParseError(f'Invalid vm instruction at line {line.line_num}":\n\n{line}\n\n"{cmd_1}" is not a valid memory segment.')

            check_offset(line.line_num, line.raw_line, line.tokens[2])

            return MEMORY_INS_MAP[cmd_0](line.line_num, line.tokens)

        elif cmd_0 in FUNCTION_INS_MAP:
            check_offset(line.line_num, line.raw_line, line.tokens[2])
            return FUNCTION_INS_MAP[cmd_0](line.line_num, line.tokens)

        else:
            raise ParseError(f'Invalid vm instruction at line {line.line_num}:\n\n{line}\n\n"{cmd_0}" is not a valid memory command.')

    else:
        raise ParseError(f'Invalid vm instruction at line {line.line_num}:\n\n{line}\n\nIllegal number of commands.')
