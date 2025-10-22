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
            'A=M-1', # select the last value in stack
            'D=M', # make copy of top of stack
            'A=M-1', # TODO: select the second to last value on the stack
            'M=D+M', # add top two values of stack and store in stack
            '@SP', # move the stack-pointer down
            'M=M-1'
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