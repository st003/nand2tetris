from parser import parse_instruction

def skip_line(line):
    """Determines if a line should be parsed."""
    if (not len(line)) or (line[0] == '/'):
        return True
    return False

def translate(lines):
    """Parses and converts Jack VM commands into Hack ASM."""

    instructions = []

    for line_num, line in enumerate(lines):
        clean_line = line.strip()

        if skip_line(clean_line):
            continue

        ins = parse_instruction(line_num, clean_line)
        instructions.append(ins)

    asm = []
    for ins in instructions:
        asm.append(ins.to_asm())

    # add infinite loop at end of program
    asm.append('// end of program\n(END)\n@END\n0;JMP')

    return asm
