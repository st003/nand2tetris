from exceptions import TranslationError

class BaseInstruction():
    """Abstract class for all instructions."""

    def __init__(self, line_num: int, parts: list[str]):
        self._line_num = line_num
        self._parts = parts
        self._asm: list[str] = []

    def to_asm(self) -> str:
        return '\n'.join(self._asm) + '\n'

# arithmetic instructions

class AddInstruction(BaseInstruction):
    """Generates the Hack ASM for the 'add' instruction."""
    def __init__(self, line_num, parts):
        self._asm = [
            '// add',
            '@SP', # deincrement stack-pointer & select new stack location
            'AM=M-1',
            'D=M', # copy value at stack-pointer
            'A=A-1', # select position below stack-pointer
            'M=D+M' # update stack with sum of both values
        ]

class SubInstruction(BaseInstruction):
    """Generates the Hack ASM for the 'sub' instruction."""
    def __init__(self, line_num, parts):
        self._asm = [
            '// sub',
            '@SP', # deincrement stack-pointer & select new stack location
            'AM=M-1',
            'D=M', # copy value at stack-pointer
            'A=A-1', # select position below stack-pointer
            'M=M-D' # update stack with difference of both values
        ]

class NegInstruction(BaseInstruction):
    """Generates the Hack ASM for the 'neg' instruction."""
    def __init__(self, line_num, parts):
        self._asm = [
            '// neg',
            '@SP', # deincrement stack-pointer & select new stack location
            'AM=M-1',
            'M=-M', # flip the sign
            '@SP', # move the stack-pointer back to the top of the stack
            'M=M+1'
        ]

# logical instructions
# TODO: numerical values represent true/false. Has to be @1 and @0, right?

class EqInstruction(BaseInstruction):
    pass

class GtInstruction(BaseInstruction):
    pass

class LtInstruction(BaseInstruction):
    pass

class AndInstruction(BaseInstruction):
    """Generates the Hack ASM for the 'and' instruction."""
    def __init__(self, line_num, parts):
        self._asm = [
            '// and',
            '@SP', # deincrement stack-pointer & select new stack location
            'AM=M-1',
            'D=M', # copy value at stack-pointer
            'A=A-1', # select position below stack-pointer
            'M=D&M' # update stack with the result of &
        ]

class OrInstruction(BaseInstruction):
    """Generates the Hack ASM for the 'or' instruction."""
    def __init__(self, line_num, parts):
        self._asm = [
            '// or',
            '@SP', # deincrement stack-pointer & select new stack location
            'AM=M-1',
            'D=M', # copy value at stack-pointer
            'A=A-1', # select position below stack-pointer
            'M=D|M' # update stack with the result of |
        ]

class NotInstruction(BaseInstruction):
    """Generates the Hack ASM for the 'not' instruction."""
    def __init__(self, line_num, parts):
        self._asm = [
            '// not',
            '@SP', # deincrement stack-pointer & select new stack location
            'AM=M-1',
            'M=!M', # flip the sign
            '@SP', # move the stack-pointer back to the top of the stack
            'M=M+1'
        ]

# memory instructions

class MemoryInstruction(BaseInstruction):
    """Abstract class for memory instructions."""

    def get_memory_segment(self) -> str:
        """Returns the memory segment name."""
        return self._parts[1]

    def get_offset(self) -> str:
        """Returns the offset value."""
        return self._parts[2]

    def get_comment(self) -> str:
        """Generates a comment line of the original VM instruction."""
        return '// ' + ' '.join(self._parts)

class PushInstruction(MemoryInstruction):
    """Generates the Hack ASM for a push instruction."""

    def __init__(self, line_num, parts):
        self._line_num = line_num
        self._parts = parts

        self._asm = [
            self.get_comment(),
            self.get_value_from_segment(),
            # This asm is the same for all memory segements
            '@SP', # select top of stack
            'A=M',
            'M=D', # set constant value to top of stack
            '@SP', # move the stack-pointer up
            'M=M+1'
        ]

    def get_static(self) -> str:
        """
        Get value from static memory segment.

        The specification says static occupies addresses 16-255, but as
        the 0-index for the stack is implementation specific, we do not
        have static-overflow checking
        """
        asm = [
            f'@static.{self.get_offset()}', # create asm variable called "static.i" (and selected it)
            'D=M' # get the value stored at that address
        ]
        return '\n'.join(asm)

    def get_constant(self) -> str:
        """Selects a constant value."""
        asm = [
            f'@{self.get_offset()}',
            'D=A'
        ]
        return '\n'.join(asm)

    def get_value_from_segment(self):
        """Selects the correct segment asm method."""
        seg = self.get_memory_segment()

        if seg == 'static':
            return self.get_static()
        elif seg == 'constant':
            return self.get_constant()
        else:
            raise TranslationError(f'Error at line {self._line_num}. Memory segement "{seg}" not recognized')

class PopInstruction(MemoryInstruction):
    """Generates the Hack ASM for a pop instruction."""

    def __init__(self, line_num, parts):
        self._line_num = line_num
        self._parts = parts

        self._asm = [
            self.get_comment(),
            '@SP',
            'AM=M-1', # deincrement stack-pointer & select new stack location
            'D=M', # make copy of selected value in the stack
            self.set_value_in_segment()
        ]

    def set_static(self) -> str:
        """
        Get address for static memory segment.

        The specification says static occupies addresses 16-255, but as
        the 0-index for the stack is implementation specific, we do not
        have static-overflow checking
        """
        asm = [
            f'@static.{self.get_offset()}', # create asm variable called "static.i" (and selected it)
            'M=D' # get the value stored at that address
        ]
        return '\n'.join(asm)

    def set_value_in_segment(self):
        """Selects the correct segment asm method."""
        seg = self.get_memory_segment()

        if seg == 'static':
            return self.set_static()
        else:
            raise TranslationError(f'Error at line {self._line_num}. Memory segement "{seg}" not recognized')
