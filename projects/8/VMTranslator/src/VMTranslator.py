import sys
import time
import traceback

from exceptions import VMTranslatorError
from file_util import get_input_lines, get_vm_files
from translator import translate

def main():

    args = sys.argv
    print('DEBUG - argv:', sys.argv)

    if (len(args) != 2):
        print('Usage: python VMTranslator.py <file.vm>|<path-to-vm-files>')
        sys.exit(1)

    try:
        start_time = time.perf_counter()

        input_path = args[1]

        vm_files, output_file_path = get_vm_files(input_path)
        input_lines, file_count = get_input_lines(vm_files)
        asm_lines = translate(input_lines, file_count)

        with open(output_file_path, 'w') as asm_file:
            asm_file.writelines(asm_lines)

        end_time: float = time.perf_counter()
        exec_time: float = round((end_time - start_time), 5)

        print(f'\nTranslation complete. Output asm exported to: {output_file_path}')
        print(f'Execution time: {exec_time} seconds\n')

    except VMTranslatorError as error:
        print(f'Error: {error}')
        sys.exit(1)

    except Exception:
        print(traceback.format_exc())
        sys.exit(2)

if __name__ == '__main__':
    main()
