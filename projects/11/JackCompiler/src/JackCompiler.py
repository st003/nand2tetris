import sys
import time
import traceback
from pathlib import Path

from CompilationEngine import CompilationEngine
from exceptions import JackCompilerError
from file_util import is_jack_file

def validate_flags(flags):
    """Validates flag string."""

    if flags[0] != '-':
        return False

    for char in flags[1:]:
        if char not in {'d', 'v'}:
            return False

    return True

def main():

    args = sys.argv
    arg_count = len(args)

    debug = False
    verbose = False
    src_path = ''

    if (arg_count < 2 or arg_count > 3):
        print('Usage: python JackCompiler.py [-d|v] <file.jack>|<path-to-jack-files-directory>')
        sys.exit(1)

    if (arg_count == 2):
        src_path = Path(args[1])

    elif (arg_count == 3):

        # NOTE: flag validation could be better
        if not validate_flags(args[1]):
            print(f"Error: '{args[1]}' is not a valid option")
            sys.exit(1)

        if 'd' in args[1]:
            debug = True

        if 'v' in args[1]:
            verbose = True

        src_path = Path(args[2])

    try:
        start_time = time.perf_counter()

        output_path = ''
        ce = None

        if src_path.is_file():
            if is_jack_file(src_path):
                output_path = src_path.parent
                ce = CompilationEngine(src_path, verbose)
                ce.compileClass()
                ce.write_vm_file()
                if debug:
                    ce.write_xml()
            else:
                raise JackCompilerError(f"File '{src_path.name}' does not have the extention '.jack'")

        else:
            output_path = src_path
            for file_path in src_path.iterdir():
                if is_jack_file(file_path):
                    ce = CompilationEngine(file_path, verbose)
                    ce.compileClass()
                    ce.write_vm_file()
                    if debug:
                        ce.write_xml()

        end_time: float = time.perf_counter()
        exec_time: float = round((end_time - start_time), 5)

        print(f'\nCompilation complete. VM files written to: {output_path}')
        print(f'Execution time: {exec_time} seconds\n')

        if debug:
            print(f'Debug - Generated debug XML output\n')

    except JackCompilerError as error:
        print(error)
        ce.write_vm_file()
        print('Generated VM output with errors')
        if debug:
            ce.write_xml()
            print('Debug - Generated XML output with errors')
        sys.exit(1)

    except Exception:
        print(traceback.format_exc())
        sys.exit(2)

if __name__ == '__main__':
    main()
