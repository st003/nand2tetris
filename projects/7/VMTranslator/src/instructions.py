class BaseInstruction():

    def __init__(self, line_num, parts):
        self._asm = []

    def to_asm(self) -> str:
        return '\n'.join(self._asm) + '\n'

# arithmetic/logical instructions

class AddInstruction(BaseInstruction):

    def __init__(self, line_num, parts):
        self._asm = [
            '// add',
            '@SP',
            'A=M', # select top of stack
            'D=M', # make copy of top of stack
            'A=M-1', # select next value in stack
            'M=M+D', # add top two values of stack and store in stack
            '@SP',
            'M=M-1' # move the stack-pointer down
        ]

class SubInstruction(BaseInstruction):
    pass

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
    pass

class PopInstruction(BaseInstruction):
    pass