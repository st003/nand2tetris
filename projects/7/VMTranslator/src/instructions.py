class BaseInstruction():

    def __init__(self, line_num, parts):
        self._asm = []

    def to_asm(self) -> str:
        return '\n'.join(self._asm) + '\n'

# arithmetic/logical instructions

class AddInstruction(BaseInstruction):
    """Generates the Hack ASM for an add command."""
    def __init__(self, line_num, parts):
        self._asm = [
            '// add',
            '@SP',
            'AM=M-1', # deincrement stack-pointer & select new stack location
            'D=M', # copy value at stack-pointer
            'A=A-1', # select position below stack-pointer
            'M=D+M' # update stack with sum of both values
        ]

class SubInstruction(BaseInstruction):
    """Generates the Hack ASM for a sub command."""
    def __init__(self, line_num, parts):
        self._asm = [
            '// sub',
            '@SP',
            'AM=M-1', # deincrement stack-pointer & select new stack location
            'D=M', # copy value at stack-pointer
            'A=A-1', # select position below stack-pointer
            'M=M-D' # update stack with difference of both values
        ]

class NegInstruction(BaseInstruction):
    # TODO: zero minus value should flip the sign
    pass

# TODO: numerical values represent true/false. Has to be @1 and @0, right?

class EqInstruction(BaseInstruction):
    pass

class GtInstruction(BaseInstruction):
    pass

class LtInstruction(BaseInstruction):
    pass

# TODO: should just be able to use the &, |, ! operations

class AndInstruction(BaseInstruction):
    pass

class OrInstruction(BaseInstruction):
    pass

class NotInstruction(BaseInstruction):
    pass

# memory instructions

class PushInstruction(BaseInstruction):
    """Generates the Hack ASM for a push command."""
    def __init__(self, line_num, parts):
        self._line_num = line_num
        self._parts = parts

        self._asm = [
            self.get_comment(),
            self.get_constant(),
            # This asm is the same for memory segements
            '@SP', # select top of stack
            'A=M',
            'M=D', # set constant value to top of stack
            '@SP', # move the stack-pointer up
            'M=M+1'
        ]

    def get_comment(self):
        """Generates a comment line of the original VM instruction."""
        return '// ' + ' '.join(self._parts)

    def get_constant(self):
        """Selects a constant value."""
        asm = [
            f'@{self._parts[2]}',
            'D=A'
        ]
        return '\n'.join(asm)

class PopInstruction(BaseInstruction):
    pass