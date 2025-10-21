import instructions as ins
from constants import ARITHMETIC_LOGICAL_INS_MAP, MEMORY_INS_MAP, MEMORY_SEGMENTS
from exceptions import ParseError

def parse_instruction(line_num: int, line: str) -> ins.BaseInstruction:
    """Parses the line and returns the associated instruction object."""

    parts = line.split(' ')

    count = len(parts)

    if count == 1:
        if parts[0] in ARITHMETIC_LOGICAL_INS_MAP:
            return ARITHMETIC_LOGICAL_INS_MAP[parts[0]](line_num, parts)
        else:
            raise ParseError(f'Invalid vm instruction "{line}" at line {line_num}. "{parts[0]}" is not a valid arithmetic/logical command.')

    elif count > 2:
        if parts[0] in MEMORY_INS_MAP:

            if parts[1] not in MEMORY_SEGMENTS:
                raise ParseError(f'Invalid vm instruction "{line}" at line {line_num}. "{parts[1]}" is not a valid memory segment.')

            try:
                offset = int(parts[2])
                if offset < 0:
                    raise ValueError(f'{offset} is less than 0')
            except ValueError:
                raise ParseError(f'Invalid vm instruction "{line}" at line {line_num}. "{parts[2]}" is not a valid offset.')

            return MEMORY_INS_MAP[parts[0]](line_num, parts[:3])
        else:
            raise ParseError(f'Invalid vm instruction "{line}" at line {line_num}. "{parts[0]}" is not a valid memory command.')

    else:
        raise ParseError(f'Invalid vm instruction "{line}" at line {line_num}. Illegal number of commands.')