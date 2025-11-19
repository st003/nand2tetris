from instructions import BootstrapInstruction, EOFInstruction
from parser import parse_instruction

def translate(input_lines, file_count=1):
    """Parses and converts Jack VM commands into Hack ASM."""

    instructions = []

    # insert bootstrap code when translating multiple files
    if file_count > 1:
        instructions.append(BootstrapInstruction())

    for i, line in enumerate(input_lines):

        if line.is_empty() or line.is_comment():
            continue

        line.line_num = i + 1
        ins = parse_instruction(line)
        instructions.append(ins)

    instructions.append(EOFInstruction())

    asm = []
    for ins in instructions:
        asm.append(ins.to_asm())

    return asm
