import sys
import time
import traceback
from pathlib import Path

from CompilationEngine import CompilationEngine
from exceptions import JackAnalyzerError
from file_util import is_jack_file

DEBUG = True # comment out before submission

def main():

    args = sys.argv

    if (len(args) != 2):
        print('Usage: python JackAnalyzer.py <file.jack>|<path-to-jack-files-directory>')
        sys.exit(1)

    try:
        start_time = time.perf_counter()

        src_path = Path(args[1])
        output_path = ''

        if src_path.is_file():
            if is_jack_file(src_path):
                output_path = src_path.parent
                ce = CompilationEngine(src_path, DEBUG)
                ce.compile()
            else:
                raise JackAnalyzerError(f"File '{src_path.name}' does not have the extention '.jack'")

        else:
            output_path = src_path
            for file_path in src_path.iterdir():
                if is_jack_file(file_path):
                    ce = CompilationEngine(file_path, DEBUG)
                    ce.compile()

        end_time: float = time.perf_counter()
        exec_time: float = round((end_time - start_time), 5)

        print(f'\nAnalysis complete. Output XMLs exported to: {output_path}')
        print(f'Execution time: {exec_time} seconds\n')

    except JackAnalyzerError as error:
        print(f'Error: {error}')
        sys.exit(1)

    except Exception:
        print(traceback.format_exc())
        sys.exit(2)

if __name__ == '__main__':
    main()
