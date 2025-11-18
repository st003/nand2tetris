from instructions import EOFInstruction
from parser import parse_instruction

def translate(input_lines):
    """Parses and converts Jack VM commands into Hack ASM."""

    instructions = []

    for i, line in enumerate(input_lines):

        if line.is_empty() or line.is_comment():
            continue

        line.line_num = i + 1
        ins = parse_instruction(line)
        instructions.append(ins)

    asm = []
    for ins in instructions:
        asm.append(ins.to_asm())
    asm.append(EOFInstruction.to_asm())

    return asm
