from exceptions import VMWriterError

class VMWriter():
    """Manages the VM commands."""

    arithmatic_map = {
        '+': 'add',
        '-': 'sub',
        '=': 'eq',
        '>': 'gt',
        '<': 'lt',
        '&': 'and',
        '|': 'or'
    }

    def __init__(self, output_path):
        self.output_path = output_path
        self._lines = []
        self.label_count = 0

    def increment_label_count(self):
        """Increments the label count by 1."""
        self.label_count += 1

    def get_segment_value(self, segment):
        """Converts the segment argument to the correct VM value."""
        if segment == 'field':
            return 'this'
        return segment

    def add_line(self, line, indent=True):
        """Adds the line to the internal lines list and adds a newline char."""
        if indent:
            self._lines.append(f'    {line}\n')
        else:
            self._lines.append(f'{line}\n')

    def close(self):
        """Write the current VM file to the output path."""
        with open(f'{self.output_path}.vm', 'w', newline='') as vm_file:
            vm_file.writelines(self._lines)

    def writePush(self, segment, index):
        """Writes a VM push command to the buffer."""
        cmd = f'push {self.get_segment_value(segment)} {index}'
        self.add_line(cmd)

    def writePop(self, segment, index):
        """Writes a VM pop command to the buffer."""
        cmd = f'pop {self.get_segment_value(segment)} {index}'
        self.add_line(cmd)

    def WriteArithmatic(self, op):
        """
        Writes a VM arithmatic command to the buffer.

        Math methods are defined at the OS level.
        """
        if op == '*':
            self.writeCall('Math.multiply', 2)
        elif op == '/':
            self.writeCall('Math.divide', 2)
        else:
            op_cmd = self.arithmatic_map.get(op)
            if op_cmd:
                self.add_line(op_cmd)
            else:
                raise VMWriterError(f"VMWriter.WriteArithmatic() - '{op}' is not a valid arithmatic operator")

    def WriteLabel(self, label_name):
        """Writes a VM label command to the buffer."""
        cmd = f'label {label_name}'
        self.add_line(cmd, indent=False)

    def WriteGoto(self, label_name):
        """Writes a VM goto command to the buffer."""
        cmd = f'goto {label_name}'
        self.add_line(cmd)

    def WriteIf(self, label_name):
        """Writes a VM if-goto command to the buffer."""
        self.add_line('not')
        cmd = f'if-goto {label_name}'
        self.add_line(cmd)

    def writeCall(self, func_name, n_args):
        """Writes a VM call command to the buffer."""
        cmd = f'call {func_name} {n_args}'
        self.add_line(cmd)

    def writeFunction(self, func_name, n_locals):
        """Writes a VM function command to the buffer."""
        cmd = f'function {func_name} {n_locals}'
        self.add_line(cmd, indent=False)

    def writeReturn(self):
        """Writes a VM return command to the buffer."""
        self.add_line('return')

    def writeKeyword(self, kwd):
        """Writes VM commands for the provided keyword to the buffer."""
        if kwd == 'true':
            # true is -1 in Hack ASM b/c all bits are 1
            self.writePush('constant', 1)
            self.add_line('neg')

        elif kwd == 'false':
            self.writePush('constant', 0)

        elif kwd == 'null':
            # TODO: implement
            pass

        elif kwd == 'this':
            self.writePush('pointer', 0)

        else:
            raise VMWriterError(f"VMWriter.writeKeyword() - '{kwd}' is not a valid keyword")

    def writeUnaryOp(self, op):
        """Writes a VM unary command to the buffer."""
        if op == '-':
            self.add_line('neg')
        elif op == '~':
            self.add_line('not')
        else:
            raise VMWriterError(f"VMWriter.writeUnaryOp() - '{op}' is not a valid unary operator")

    def writeComment(self, comment):
        """Writes a VM comment to the buffer."""
        cmt = f'// {comment}'
        self.add_line(cmt, indent=False)

    def writeStringConstant(self, string):
        """
        Writes all VM commands needed for the given string.

        Built-in String function defined at OS level.
        """
        # String.new() first arg is the max length of the string constant
        self.writePush('constant', len(string))
        self.writeCall('String.new', 1)
        for char in string:
            self.writePush('constant', ord(char)) # get ASCII decimal value of char
            # NOTE: why is nArgs always 2?
            # the max length is **probably** to the first arg
            # and the ASCII representation of the char is the second arg
            self.writeCall('String.appendChar', 2)
