import sys
import time
import traceback

from exceptions import JackAnalyzerError

def main():

    args = sys.argv

    if (len(args) != 2):
        print('Usage: python JackAnalyzer.py <path-to-jack-files-directory>')
        sys.exit(1)

    try:
        start_time = time.perf_counter()

        input_path = args[1]

        # TODO: call the compilation engine once for each .jack file
        # in the input directory

        end_time: float = time.perf_counter()
        exec_time: float = round((end_time - start_time), 5)

        print(f'\nAnalysis complete. Output XMLs exported to: {input_path}')
        print(f'Execution time: {exec_time} seconds\n')

    except JackAnalyzerError as error:
        print(f'Error: {error}')
        sys.exit(1)

    except Exception:
        print(traceback.format_exc())
        sys.exit(2)

if __name__ == '__main__':
    main()
