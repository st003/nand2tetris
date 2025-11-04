import sys
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
        input_file_path = args[1]

        parent_dirs, file_name = get_vm_file_name(input_file_path)

        input_lines = []
        with open(input_file_path, 'r') as vm_file:
            input_lines = vm_file.readlines()

        asm_lines = translate(input_lines)

        with open(f'{parent_dirs}/{file_name}.asm', 'w') as asm_file:
            asm_file.writelines(asm_lines)

    except VMTranslatorError as error:
        print(f'Error: {error}')
        sys.exit(1)

    except Exception:
        print(traceback.format_exc())
        sys.exit(2)

if __name__ == '__main__':
    main()
