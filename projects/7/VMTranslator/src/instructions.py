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
            'A=A-1', # select position stack-pointer - 1
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
            'A=A-1', # select position stack-pointer - 1
            'M=M-D' # update stack with difference of both values
        ]

class NegInstruction(BaseInstruction):
    pass

class EqInstruction(BaseInstruction):
    pass

class GtInstruction(BaseInstruction):
    pass

class LtInstruction(BaseInstruction):
    pass

class AndInstruction(BaseInstruction):
    pass

class OrInstruction(BaseInstruction):
    pass

class NotInstruction(BaseInstruction):
    pass

# memory instructions

class PushInstruction(BaseInstruction):

    def __init__(self, line_num, parts):
        self._line_num = line_num
        self._parts = parts

        self._asm = [
            self.get_comment(),
            # TODO: this works only with constant
            f'@{parts[2]}', # select constant value
            'D=A',
            '@SP', # select top of stack
            'A=M',
            'M=D', # set constant value to top of stack
            '@SP', # move the stack-pointer up
            'M=M+1'
        ]

    def get_comment(self):
        return '// ' + ' '.join(self._parts)

class PopInstruction(BaseInstruction):
    pass