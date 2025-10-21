from instructions import BaseInstruction
from parser import parse_instruction

def skip_line(line: str) -> bool:
    """Determines if a line should be parsed."""
    if (not len(line)) or (line[0] == '/'):
        return True
    return False

def translate(lines: list[str]) -> list[str]:
    """Parses and converts Jack VM commands into Hack ASM."""

    instructions: list[BaseInstruction] = []

    for line_num, line in enumerate(lines):
        clean_line = line.strip().lower()

        if skip_line(clean_line):
            continue

        ins = parse_instruction(line_num, clean_line)
        instructions.append(ins)

    asm: list[str] = []
    for ins in instructions:
        asm.append(ins.to_asm())

    return asm
