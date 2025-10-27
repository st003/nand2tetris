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
# NOTE: Hack ASM uses -1 as true and 0 as false

class EqInstruction(BaseInstruction):
    """Generates the Hack ASM for the 'eq' instruction."""
    def __init__(self, line_num, parts):
        self._asm = [
            '// eq',
            '@SP', # deincrement stack-pointer & select new stack location
            'AM=M-1',
            'D=M', # copy value at stack-pointer
            '@SP', # deincrement stack-pointer again & select new stack location
            'AM=M-1',
            'D=M-D', # diff selected values
            f'@TRUE.{line_num}', # if diff is 0, jump to true
            'D;JEQ',
            '@SP', # else, set to false and jump to end
            'A=M',
            'M=0',
            f'@END.{line_num}',
            '0;JMP',
            f'(TRUE.{line_num})', # set to true
            '@SP',
            'A=M',
            'M=-1',
            f'(END.{line_num})', # increment the stack-pointer
            '@SP',
            'M=M+1'
        ]

class GtInstruction(BaseInstruction):
    """Generates the Hack ASM for the 'gt' instruction."""
    def __init__(self, line_num, parts):
        self._asm = [
            '// gt',
            '@SP', # deincrement stack-pointer & select new stack location
            'AM=M-1',
            'D=M', # copy value at stack-pointer
            '@SP', # deincrement stack-pointer again & select new stack location
            'AM=M-1',
            'D=M-D', # diff selected values
            f'@TRUE.{line_num}', # if D is greater-than 0, jump to true
            'D;JGT',
            '@SP', # else, set to false and jump to end
            'A=M',
            'M=0',
            f'@END.{line_num}',
            '0;JMP',
            f'(TRUE.{line_num})', # set to true
            '@SP',
            'A=M',
            'M=-1',
            f'(END.{line_num})', # increment the stack-pointer
            '@SP',
            'M=M+1'
        ]

class LtInstruction(BaseInstruction):
    """Generates the Hack ASM for the 'lt' instruction."""
    def __init__(self, line_num, parts):
        self._asm = [
            '// lt',
            '@SP', # deincrement stack-pointer & select new stack location
            'AM=M-1',
            'D=M', # copy value at stack-pointer
            '@SP', # deincrement stack-pointer again & select new stack location
            'AM=M-1',
            'D=M-D', # diff selected values
            f'@TRUE.{line_num}', # if D is less-than 0, jump to true
            'D;JLT',
            '@SP', # else, set to false and jump to end
            'A=M',
            'M=0',
            f'@END.{line_num}',
            '0;JMP',
            f'(TRUE.{line_num})', # set to true
            '@SP',
            'A=M',
            'M=-1',
            f'(END.{line_num})', # increment the stack-pointer
            '@SP',
            'M=M+1'
        ]

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

    TEMP_INDEX = 5
    TEMP_MAX_OFFSET = 8

    symbols = {
        'argument': 'ARG',
        'local': 'LCL',
        'this': 'THIS',
        'that': 'THAT'
    }

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
            'M=D', # set selected value to top of stack
            '@SP', # increment the stack-pointer
            'M=M+1'
        ]

    def get_constant(self) -> str:
        """Selects a constant value."""
        asm = [
            f'@{self.get_offset()}',
            'D=A'
        ]
        return '\n'.join(asm)

    def get_static(self) -> str:
        """
        Get value from static memory segment.

        The specification says static occupies addresses 16-255, but as
        the 0-index for the stack is implementation specific, we do not
        have static-overflow checking.
        """
        asm = [
            f'@static.{self.get_offset()}', # create asm variable called "static.i" (and selected it)
            'D=M' # get the value stored at that address
        ]
        return '\n'.join(asm)

    def get_temp(self):
        """
        Get value from temp memory segment.

        The specification says temp occupies addresses 5-12
        """

        offset = self.get_offset()

        if int(offset) > self.TEMP_MAX_OFFSET:
            raise TranslationError(f'at line {self._line_num}. Offset my not be greater than {self.TEMP_MAX_OFFSET} for temp')

        asm = [
            f'@{self.get_offset()}', # get the offset as a literal number
            'D=A',
            f'@{self.TEMP_INDEX}', # select value at segment temp-index + offset
            'A=D+A',
            'D=M' # copy value from segment temp-index + offset
        ]
        return '\n'.join(asm)

    def get_value_by_segment_name(self):
        """Get value from memory segment."""
        asm = [
            f'@{self.get_offset()}', # get the offset as a literal number
            'D=A',
            f'@{self.symbols[self.get_memory_segment()]}', # select value at segment 0-index + offset
            'A=D+M',
            'D=M' # copy value from segment 0-index + offset
        ]
        return '\n'.join(asm)

    def get_value_from_segment(self):
        """Selects the correct segment asm method."""
        seg = self.get_memory_segment()

        if seg in self.symbols:
            return self.get_value_by_segment_name()
        elif seg == 'constant':
            return self.get_constant()
        elif seg == 'static':
            return self.get_static()
        elif seg == 'temp':
            return self.get_temp()
        else:
            raise TranslationError(f'at line {self._line_num}. Memory segement "{seg}" not recognized')

class PopInstruction(MemoryInstruction):
    """Generates the Hack ASM for a pop instruction."""

    def __init__(self, line_num, parts):
        self._line_num = line_num
        self._parts = parts

        self._asm = [
            self.get_comment(),
            self.get_segement_address(),
            '@SP',
            'AM=M-1', # deincrement stack-pointer & select new stack location
            'D=M', # make copy of selected value from the stack
            '@R13', # select segment address stored at R13
            'A=M',
            'M=D' # store value from stack into memory segment
        ]

    def get_address_by_segment_name(self):
        """Get address for memory segment."""
        asm = [
            f'@{self.get_offset()}', # get the offset as a literal number
            'D=A',
            f'@{self.symbols[self.get_memory_segment()]}', # calculate addr = symbol + offset
            'D=D+M',
            '@R13', # store addr in R13 (non-reserved register)
            'M=D'
        ]
        return '\n'.join(asm)

    def get_static(self) -> str:
        """
        Get address for static memory segment.

        The specification says static occupies addresses 16-255, but as
        the 0-index for the stack is implementation specific, we do not
        have static-overflow checking
        """
        asm = [
            f'@static.{self.get_offset()}', # create asm variable called "static.i" (and selected it)
            'D=A', # copy that address in R13
            '@R13',
            'M=D'
        ]
        return '\n'.join(asm)

    def get_segement_address(self):
        """Selects the correct segment asm method."""
        seg = self.get_memory_segment()

        if seg in self.symbols:
            return self.get_address_by_segment_name()
        elif seg == 'static':
            return self.get_static()
        else:
            raise TranslationError(f'Error at line {self._line_num}. Memory segement "{seg}" not recognized')
