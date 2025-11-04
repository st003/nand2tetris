import sys
import time
import traceback

from exceptions import VMTranslatorError
from translator import translate
from utils import get_vm_file_name

def main():

    args = sys.argv

    if (len(args) != 2):
        print('Usage: python VMTranslator.py')
        sys.exit(1)

    try:
        start_time = time.perf_counter()

        input_file_path = args[1]

        parent_dirs, file_name = get_vm_file_name(input_file_path)

        input_lines = []
        with open(input_file_path, 'r') as vm_file:
            input_lines = vm_file.readlines()

        asm_lines = translate(input_lines)

        output_file_path = f'{parent_dirs}/{file_name}.asm'
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
