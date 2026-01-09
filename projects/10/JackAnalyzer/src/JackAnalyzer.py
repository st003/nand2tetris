import sys
import time
import traceback
from pathlib import Path

from CompilationEngine import CompilationEngine
from exceptions import JackAnalyzerError
from file_util import is_jack_file

def main():

    args = sys.argv
    arg_count = len(args)

    debug = False
    src_path = ''

    if (arg_count < 2 or arg_count > 3):
        print('Usage: python JackAnalyzer.py [-d] <file.jack>|<path-to-jack-files-directory>')
        sys.exit(1)

    if (arg_count == 2):
        src_path = Path(args[1])

    elif (arg_count == 3):

        if args[1] != '-d':
            print(f"Error: '{args[1]}' is not a valid option")
            sys.exit(1)

        debug = True
        src_path = Path(args[2])

    try:
        start_time = time.perf_counter()

        output_path = ''
        ce = None

        if src_path.is_file():
            if is_jack_file(src_path):
                output_path = src_path.parent
                ce = CompilationEngine(src_path, debug)
                ce.compile()
            else:
                raise JackAnalyzerError(f"File '{src_path.name}' does not have the extention '.jack'")

        else:
            output_path = src_path
            for file_path in src_path.iterdir():
                if is_jack_file(file_path):
                    ce = CompilationEngine(file_path, debug)
                    ce.compileClass()
                    ce.write_xml()

        end_time: float = time.perf_counter()
        exec_time: float = round((end_time - start_time), 5)

        print(f'\nAnalysis complete. Output XMLs exported to: {output_path}')
        print(f'Execution time: {exec_time} seconds\n')

    except JackAnalyzerError as error:
        print(error)
        if debug:
            ce.write_xml()
            print('\nDebug - wrote XML output with errors')
        sys.exit(1)

    except Exception:
        print(traceback.format_exc())
        sys.exit(2)

if __name__ == '__main__':
    main()
