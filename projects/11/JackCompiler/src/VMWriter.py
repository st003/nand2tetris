# TODO: api implementation def found at: 5.10 @13:27

# TODO: Average:
# call main
# local variable declaration
# arrays (declaration and access)
# let statements
# function calling
# while loops
# return statements

class VMWriter():

    def __init__(self, output_path):
        self.output_path = output_path
        self._lines = []

    def writePush(self, segment, index):
        """Writes a VM push command to the buffer."""
        cmd = f'push {segment} {index}'
        self._lines.append(cmd)

    def writePop(self, segment, index):
        """Writes a VM pop command to the buffer."""
        cmd = f'pop {segment} {index}'
        self._lines.append(cmd)

    def WriteArithmatic(self):
        # TODO: implement
        pass

    def WriteLabel(self):
        # TODO: implement
        pass

    def WriteGoto(self):
        # TODO: implement
        pass

    def WriteIf(self):
        # TODO: implement
        pass

    def writeCall(self):
        # TODO: implement
        pass

    def writeFunction(self):
        # TODO: implement
        pass

    def writeReturn(self):
        # TODO: implement
        pass

    def writeComment(self, comment):
        """Writes a VM comment to the buffer."""
        cmt = f'// {comment}'
        self._lines.append(cmt)

    def close(self):
        """Write the current VM file to the output path."""
        with open(f'{self.output_path}.vm', 'w', newline='') as vm_file:
            vm_file.writelines(self._lines)
