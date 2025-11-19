from exceptions import TranslationError
from file_util import Line

class BaseInstruction():
    """Abstract class for all instructions."""

    def __init__(self, line):
        self._line = line
        self._asm = []

    def get_file_name(self):
        return self._line.file_name

    def get_raw_line(self):
        return self._line.raw_line

    def get_line_num(self):
        return self._line.line_num

    def get_tokens(self):
        return self._line.tokens

    def get_comment(self):
        """Generates a comment line of the original VM instruction."""
        return '// ' + ' '.join(self.get_tokens())

    def to_asm(self):
        return '\n'.join(self._asm) + '\n'

# ARITHMATIC INSTRUCTIONS

class AddInstruction(BaseInstruction):
    """Generates the Hack ASM for the 'add' instruction."""
    def __init__(self, line):
        super().__init__(line)
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
    def __init__(self, line):
        super().__init__(line)
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
    def __init__(self, line):
        super().__init__(line)
        self._asm = [
            '// neg',
            '@SP', # deincrement stack-pointer & select new stack location
            'AM=M-1',
            'M=-M', # flip the sign
            '@SP', # move the stack-pointer back to the top of the stack
            'M=M+1'
        ]

# LOGICAL INSTRUCTIONS
# NOTE: Hack ASM uses -1 as true and 0 as false

class EqInstruction(BaseInstruction):
    """Generates the Hack ASM for the 'eq' instruction."""
    def __init__(self, line):
        super().__init__(line)
        self._asm = [
            '// eq',
            '@SP', # deincrement stack-pointer & select new stack location
            'AM=M-1',
            'D=M', # copy value at stack-pointer
            '@SP', # deincrement stack-pointer again & select new stack location
            'AM=M-1',
            'D=M-D', # diff selected values
            f'@TRUE.{self.get_line_num()}', # if diff is 0, jump to true
            'D;JEQ',
            '@SP', # else, set to false and jump to end
            'A=M',
            'M=0',
            f'@END.{self.get_line_num()}',
            '0;JMP',
            f'(TRUE.{self.get_line_num()})', # set to true
            '@SP',
            'A=M',
            'M=-1',
            f'(END.{self.get_line_num()})', # increment the stack-pointer
            '@SP',
            'M=M+1'
        ]

class GtInstruction(BaseInstruction):
    """Generates the Hack ASM for the 'gt' instruction."""
    def __init__(self, line):
        super().__init__(line)
        self._asm = [
            '// gt',
            '@SP', # deincrement stack-pointer & select new stack location
            'AM=M-1',
            'D=M', # copy value at stack-pointer
            '@SP', # deincrement stack-pointer again & select new stack location
            'AM=M-1',
            'D=M-D', # diff selected values
            f'@TRUE.{self.get_line_num()}', # if D is greater-than 0, jump to true
            'D;JGT',
            '@SP', # else, set to false and jump to end
            'A=M',
            'M=0',
            f'@END.{self.get_line_num()}',
            '0;JMP',
            f'(TRUE.{self.get_line_num()})', # set to true
            '@SP',
            'A=M',
            'M=-1',
            f'(END.{self.get_line_num()})', # increment the stack-pointer
            '@SP',
            'M=M+1'
        ]

class LtInstruction(BaseInstruction):
    """Generates the Hack ASM for the 'lt' instruction."""
    def __init__(self, line):
        super().__init__(line)
        self._asm = [
            '// lt',
            '@SP', # deincrement stack-pointer & select new stack location
            'AM=M-1',
            'D=M', # copy value at stack-pointer
            '@SP', # deincrement stack-pointer again & select new stack location
            'AM=M-1',
            'D=M-D', # diff selected values
            f'@TRUE.{self.get_line_num()}', # if D is less-than 0, jump to true
            'D;JLT',
            '@SP', # else, set to false and jump to end
            'A=M',
            'M=0',
            f'@END.{self.get_line_num()}',
            '0;JMP',
            f'(TRUE.{self.get_line_num()})', # set to true
            '@SP',
            'A=M',
            'M=-1',
            f'(END.{self.get_line_num()})', # increment the stack-pointer
            '@SP',
            'M=M+1'
        ]

class AndInstruction(BaseInstruction):
    """Generates the Hack ASM for the 'and' instruction."""
    def __init__(self, line):
        super().__init__(line)
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
    def __init__(self, line):
        super().__init__(line)
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
    def __init__(self, line):
        super().__init__(line)
        self._asm = [
            '// not',
            '@SP', # deincrement stack-pointer & select new stack location
            'AM=M-1',
            'M=!M', # flip the sign
            '@SP', # move the stack-pointer back to the top of the stack
            'M=M+1'
        ]

# BRANCHING INSTRUCTIONS

class BranchingBaseInstruction(BaseInstruction):
    """Base instruction for Branching instructions."""
    def make_label_name(self):

        func_name = self.get_file_name()
        if FunctionBaseInstruction.calling_function:
            func_name = FunctionBaseInstruction.calling_function

        label_name = self.get_tokens()[1]
        return f'{func_name}${label_name}'

class GotoInstruction(BranchingBaseInstruction):
    """Generates the Hack ASM for the 'goto' instruction."""
    def __init__(self, line):
        super().__init__(line)
        self._asm = [
            '// goto',
            f'@{self.make_label_name()}', # jump to label
            '0;JMP'
        ]

class IfGotoInstruction(BranchingBaseInstruction):
    """
    Generates the Hack ASM for the 'if-goto' instruction.

    Implementation is jump to the label of the last values in the
    stack is NOT zero.

    Note: this seems to contradict the lecture which state we should
    expect a boolean expression immediately before the if-goto
    """
    def __init__(self, line):
        super().__init__(line)
        self._asm = [
            '// if-goto',
            '@SP', # deincrement stack-pointer & select new top value in stack
            'AM=M-1',
            'D=M', # move it into d for evaluation
            f'@{self.make_label_name()}',
            'D;JNE'
        ]

class LabelInstruction(BranchingBaseInstruction):
    """Generates the Hack ASM for the 'label' instruction."""
    def __init__(self, line):
        super().__init__(line)
        self._asm = [
            '// label',
            f'({self.make_label_name()})' # write label
        ]

# FUNCTION INSTRUCTIONS

class FunctionBaseInstruction(BaseInstruction):
    """Abstract class for function instructions."""
    calling_function = ''

class CallInstruction(FunctionBaseInstruction):
    """Generates Hack ASM for 'call' instruction."""

    def __init__(self, line):
        super().__init__(line)
        self._asm = [
            self.get_comment(),
            '// start initialization of function call',
            '// create temp backup of new argument 0',
            self.calculate_new_argument_segment(),
            f'@{self.calling_function}$ret.{self.get_line_num()}',
            'D=A',
            '@SP',
            'A=M',
            'M=D',
            '// backup local pointer',
            '@LCL',
            'D=M',
            '@SP',
            'AM=M+1',
            'M=D',
            '// backup argument pointer',
            '@ARG',
            'D=M',
            '@SP',
            'AM=M+1',
            'M=D',
            '// backup this pointer',
            '@THIS',
            'D=M',
            '@SP',
            'AM=M+1',
            'M=D',
            '// backup that pointer',
            '@THAT',
            'D=M',
            '@SP',
            'AM=M+1',
            'M=D',
            '// set new argument 0',
            '@R14', # get temp backup of new argument 0
            'D=M',
            '@ARG',
            'M=D',
            '// increment stack-pointer',
            '@SP',
            'M=M+1', # stack-pointer should now be pointing to the top of the stack
            '// jump to function definition',
            f'@{self.get_tokens()[1]}',
            '0;JMP',
            '// return address for called function',
            f'({self.calling_function}$ret.{self.get_line_num()})',
            '// end initialization of function call'
        ]

    def calculate_new_argument_segment(self):
        """
        Calculate and store the address for the new argument 0 pointer.

        In the case where the function is called with 0 arguments, create
        space on the stack for storing the eventual return value so as not
        to overwrite the return address.
        """

        if int(self.get_tokens()[2]) == 0:
            asm = [
                '// handle case where function was called with 0 arguments',
                '@SP', # increment the stack-pointer
                'AM=M+1',
                f'@1', # specify the new empty spot in the stack as your argument 0
                'D=A',
                '@SP',
                'D=M-D',
                '@R14', # temp backup of new argument 0
                'M=D'
            ]

        else:
            asm = [
                f'@{self.get_tokens()[2]}', # calculate the address of new argument 0
                'D=A',
                '@SP',
                'D=M-D',
                '@R14', # temp backup of new argument 0
                'M=D'
            ]

        return '\n'.join(asm)

class FunctionInstruction(FunctionBaseInstruction):
    """Generates Hack ASM for 'function' instruction."""

    def __init__(self, line):
        super().__init__(line)

        # track the current function scope for generating return labels
        FunctionBaseInstruction.calling_function = self.get_tokens()[1]

        self._asm = [
            '', # add leading space in asm output
            self.get_comment(),
            f'({self.get_tokens()[1]})',
            '// start local segment initialization',
            '@SP', # grab the current stack pointer address...
            'D=M',
            '@LCL', # copy it to the local pointer and go to the top of the stack
            'AM=D',
            self.zero_out_local_variables(), # zero out n-number local variables
            '// end local segment initialization'
        ]

    def zero_out_local_variables(self):
        """Initialize n zero onto the stack values."""
        local_segment_asm = [f'// zero-out {self.get_tokens()[2]} local variables\n']

        for i in range(int(self.get_tokens()[2])):

            line = Line(self.get_file_name(), 'push constant 0')
            line.line_num = self.get_line_num()
            line.tokens = ['push', 'constant', '0']

            ins = PushInstruction(line).to_asm()
            local_segment_asm.append(ins)

        return ''.join(local_segment_asm).rstrip()

class ReturnInstruction(FunctionBaseInstruction):
    """Generates Hack ASM for 'return' instruction."""
    def __init__(self, line):
        super().__init__(line)

        pop_ins = Line(self.get_file_name(), 'pop argument 0')
        pop_ins.line_num = self.get_line_num()
        pop_ins.tokens = ['pop', 'argument', '0']

        self._asm = [
            self.get_comment(),
            '// copy return value to argument 0',
            PopInstruction(pop_ins).to_asm().rstrip(),
            '// restore segment pointers for caller function',
            '@LCL', # move stack-pointer to that local - 1
            'D=M',
            '// restore that pointer',
            '@SP',
            'AM=D-1',
            'D=M',
            '@THAT',
            'M=D',
            '// restore this pointer',
            '@SP',
            'AM=M-1',
            'D=M',
            '@THIS',
            'M=D',
            '// restore argument pointer',
            '// backup current location of argument',
            '@ARG',
            'D=M',
            '@R14', # temp backup of current arg pointer
            'M=D',
            '// now restore argument pointer',
            '@SP',
            'AM=M-1',
            'D=M',
            '@ARG',
            'M=D',
            '// restore local pointer',
            '@SP',
            'AM=M-1',
            'D=M',
            '@LCL',
            'M=D',
            '// temp backup return address',
            '@SP',
            'AM=M-1',
            'D=M',
            '@R15', # temp backup of return address value
            'M=D',
            '// clear function working stack',
            '@R14', # get backup of arg pointer
            'D=M',
            '@SP', # move stack-pointer to location just after return value
            'AM=D+1',
            '// Jump to return address',
            '@R15', # get the address stored in R15
            'A=M',
            '0;JMP' # and jump to it
        ]

# MEMORY INSTRUCTIONS

class MemoryInstruction(BaseInstruction):
    """Abstract class for memory instructions."""

    POINTER_MAX = 1
    POINTER_MAP = {
        '0': 'THIS',
        '1': 'THAT',
    }

    TEMP_INDEX = 5
    TEMP_MAX_OFFSET = 8

    symbols = {
        'argument': 'ARG',
        'local': 'LCL',
        'this': 'THIS',
        'that': 'THAT'
    }

    def get_memory_segment(self):
        """Returns the memory segment name."""
        return self.get_tokens()[1]

    def get_offset(self):
        """Returns the offset value."""
        return self.get_tokens()[2]

class PushInstruction(MemoryInstruction):
    """Generates the Hack ASM for a push instruction."""

    def __init__(self, line):
        super().__init__(line)
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

    def get_constant(self):
        """Selects a constant value."""
        asm = [
            f'@{self.get_offset()}',
            'D=A'
        ]
        return '\n'.join(asm)

    def get_pointer(self):
        """
        Get value from pointer memory segment.

        The specification says the offset maps to either THIS or THAT.

        0 = THIS
        1 = THAT

        As a result, the offset cannot be greater than 1.
        """
        offset = self.get_offset()

        if int(offset) > self.POINTER_MAX:
            raise TranslationError(f'at line {self.get_line_num()}. Offset may not be greater than {self.POINTER_MAX} for pointer')

        asm = [
            f'@{self.POINTER_MAP[offset]}', # select THIS or THAT
            'D=M' # copy the value stored in THIS or THAT
        ]
        return '\n'.join(asm)

    def get_static(self):
        """
        Get value from static memory segment.

        The specification says static occupies addresses 16-255, but as
        the 0-index for the stack is implementation specific, we do not
        have static-overflow checking.
        """
        asm = [
            f'@{self.get_file_name()}.{self.get_offset()}', # create asm variable called "static.i" (and selected it)
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
            raise TranslationError(f'at line {self.get_line_num()}. Offset may not be greater than {self.TEMP_MAX_OFFSET} for temp')

        asm = [
            f'@{self.get_offset()}', # get the offset as a literal number
            'D=A',
            f'@{self.TEMP_INDEX}', # select value at segment temp-index + offset
            'A=D+A',
            'D=M' # copy value from segment temp-index + offset
        ]
        return '\n'.join(asm)

    def get_value_from_segment(self):
        """Selects the correct segment asm method."""
        seg = self.get_memory_segment()

        if seg in self.symbols:
            return self.get_value_by_segment_name()
        elif seg == 'constant':
            return self.get_constant()
        elif seg == 'pointer':
            return self.get_pointer()
        elif seg == 'static':
            return self.get_static()
        elif seg == 'temp':
            return self.get_temp()
        else:
            raise TranslationError(f'at line {self.get_line_num()}. Memory segement "{seg}" not recognized')

class PopInstruction(MemoryInstruction):
    """Generates the Hack ASM for a pop instruction."""

    def __init__(self, line):
        super().__init__(line)
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

    def get_pointer(self):
        """
        Get address for pointer memory segment.

        The specification says the offset maps to either THIS or THAT.

        0 = THIS
        1 = THAT

        As a result, the offset cannot be greater than 1.
        """
        offset = self.get_offset()

        if int(offset) > self.POINTER_MAX:
            raise TranslationError(f'at line {self.get_line_num()}. Offset may not be greater than {self.POINTER_MAX} for pointer')

        asm = [
            f'@{self.POINTER_MAP[offset]}', # select THIS or THAT
            'D=A', # copy the address for THIS or THAT
            '@R13', # and backup into R13 (non-reserved register)
            'M=D'
        ]
        return '\n'.join(asm)

    def get_static(self):
        """
        Get address for static memory segment.

        The specification says static occupies addresses 16-255, but as
        the 0-index for the stack is implementation specific, we do not
        have static-overflow checking
        """
        asm = [
            f'@{self.get_file_name()}.{self.get_offset()}', # create asm variable called "static.i" (and selected it)
            'D=A', # copy that address in R13
            '@R13',
            'M=D'
        ]
        return '\n'.join(asm)

    def get_temp(self):
        """
        Get address for temp memory segment.

        The specification says temp occupies addresses 5-12
        """

        offset = self.get_offset()

        if int(offset) > self.TEMP_MAX_OFFSET:
            raise TranslationError(f'at line {self.get_line_num()}. Offset may not be greater than {self.TEMP_MAX_OFFSET} for temp')

        asm = [
            f'@{self.get_offset()}', # get the offset as a literal number
            'D=A',
            f'@{self.TEMP_INDEX}', # calculate addr = temp-index + offset
            'D=D+A',
            '@R13', # store addr in R13 (non-reserved register)
            'M=D'
        ]
        return '\n'.join(asm)

    def get_segement_address(self):
        """Selects the correct segment asm method."""
        seg = self.get_memory_segment()

        if seg in self.symbols:
            return self.get_address_by_segment_name()
        elif seg == 'pointer':
            return self.get_pointer()
        elif seg == 'static':
            return self.get_static()
        elif seg == 'temp':
            return self.get_temp()
        else:
            raise TranslationError(f'Error at line {self.get_line_num()}. Memory segement "{seg}" not recognized')

# utility instructions

class BootstrapInstruction():
    """Code for booting the program."""
    def to_asm(self):
        asm = [
            '// bootstrap code',
            '// set the base stack-pointer to 256',
            '@256',
            'D=A',
            '@SP',
            'M=D',
            '// jump to Sys.init function',
            '@Sys.init',
            '0;JMP'
        ]
        return '\n'.join(asm) + '\n'

class EOFInstruction():
    """Infinite loop for the end of the program."""
    def to_asm(self):
        asm = [
            '\n// END OF PROGRAM',
            '(EOF)',
            '@EOF',
            '0;JMP'
        ]
        return '\n'.join(asm) + '\n'
