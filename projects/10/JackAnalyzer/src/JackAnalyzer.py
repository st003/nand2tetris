import sys
import time
import traceback
from pathlib import Path

from CompilationEngine import CompilationEngine
from exceptions import JackAnalyzerError
from file_util import is_jack_file

def main():

    args = sys.argv

    if (len(args) != 2):
        print('Usage: python JackAnalyzer.py <path-to-jack-files-directory>')
        sys.exit(1)

    try:
        start_time = time.perf_counter()

        src_dir = Path(args[1])
        for file_path in src_dir.iterdir():
            if is_jack_file(file_path):
                ce = CompilationEngine(file_path)
                ce.compile()

        end_time: float = time.perf_counter()
        exec_time: float = round((end_time - start_time), 5)

        print(f'\nAnalysis complete. Output XMLs exported to: {src_dir}')
        print(f'Execution time: {exec_time} seconds\n')

    except JackAnalyzerError as error:
        print(f'Error: {error}')
        sys.exit(1)

    except Exception:
        print(traceback.format_exc())
        sys.exit(2)

if __name__ == '__main__':
    main()
