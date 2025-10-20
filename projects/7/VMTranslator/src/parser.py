import instructions as ins
from exceptions import ParseError

ARITHEMIC_LOGICAL_INS_MAP = {
    'add': ins.AddInstruction,
    'sub': ins.SubInstruction,
    'neg': ins.NegInstruction,
    'eq': ins.EqInstruction,
    'gt': ins.GtInstruction,
    'lt': ins.LtInstruction,
    'and': ins.AndInstruction,
    'or': ins.OrInstruction,
    'not': ins.NotInstruction
}

def parse_instruction(line_num: int, line: str) -> ins.BaseInstruction:
    """Parses the line and returns the associated instruction object."""

    parts = line.split(' ')

    count = len(parts)

    if count == 1:
        if parts[0] in ARITHEMIC_LOGICAL_INS_MAP:
            return ARITHEMIC_LOGICAL_INS_MAP[parts[0]](line_num, parts)
        else:
            raise ParseError(f'Invalid vm instruction "{line}" at line {line_num}. "{parts[0]}" is not a valid arithmetic/logical command.')

    elif count > 2:
        # TODO: slice the first 3 and check each part
        return ins.BaseInstruction(1, 'todo')

    else:
        raise ParseError(f'Invalid vm instruction "{line}" at line {line_num}. Illegal number of commands.')