from exceptions import ParseError

def parse_instruction(line_num: int, line: str):

    parts = line.split(' ')

    count = len(parts)
    if count == 2:
        raise ParseError(f'Invalid vm instruction "{line}" at line {line_num}')

    if count == 1:
        # TODO: check this is a valid arithmetic command
        pass

    if count == 3:
        # TODO: check each part
        pass

    # TODO: return the correct instruction object