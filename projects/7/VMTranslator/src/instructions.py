from exceptions import TranslationError

class BaseInstruction():
    """Abstract class for all instructions."""

    def __init__(self, line_num, parts):
        self._line_num = line_num
        self._parts = parts
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
    """Generates the Hack ASM for a push command."""

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
            raise TranslationError(f'Memory segement "{seg}" not recognized')

class PopInstruction(MemoryInstruction):
    pass
