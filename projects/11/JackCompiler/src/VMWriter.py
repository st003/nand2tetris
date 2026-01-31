from exceptions import VMWriterError

# TODO: api implementation def found at: 5.10 @13:27

class VMWriter():

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

    def add_line(self, line):
        """Adds the line to the internal lines list and adds a newline char."""
        self._lines.append(f'{line}\n')

    def close(self):
        """Write the current VM file to the output path."""
        with open(f'{self.output_path}.vm', 'w', newline='') as vm_file:
            vm_file.writelines(self._lines)

    def writePush(self, segment, index):
        """Writes a VM push command to the buffer."""
        cmd = f'push {segment} {index}'
        self.add_line(cmd)

    def writePop(self, segment, index):
        """Writes a VM pop command to the buffer."""
        cmd = f'pop {segment} {index}'
        self.add_line(cmd)

    def WriteArithmatic(self, op):
        """Writes a VM arithmatic command to the buffer."""
        if op == '*':
            # TODO: implement
            pass
        elif op == '/':
            # TODO: implement
            pass
        else:
            opCmd = self.arithmatic_map.get(op)
            if opCmd:
                self.add_line(opCmd)
            else:
                raise VMWriterError(f"VMWriter.WriteArithmatic() - '{op}' is not a valid arithatic operator")

    def WriteLabel(self, label_name):
        """Writes a VM label command to the buffer."""
        cmd = f'label {label_name}'
        self.add_line(cmd)

    def WriteGoto(self, label_name):
        """Writes a VM goto command to the buffer."""
        cmd = f'goto {label_name}'
        self.add_line(cmd)

    def WriteIf(self, label_name):
        """Writes a VM if-goto command to the buffer."""
        self.add_line('not')
        cmd = f'if-goto {label_name}'
        self.add_line(cmd)

    def writeCall(self, func_name, nArgs):
        """Writes a VM call command to the buffer."""
        cmd = f'call {func_name} {nArgs}'
        self.add_line(cmd)

    def writeFunction(self, func_name, nLocals):
        """Writes a VM function command to the buffer."""
        cmd = f'function {func_name} {nLocals}'
        self.add_line(cmd)

    def writeReturn(self):
        # TODO: implement
        pass

    def writeComment(self, comment):
        """Writes a VM comment to the buffer."""
        cmt = f'// {comment}'
        self.add_line(cmt)

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
