import sys
import traceback

from exceptions import VMTranslatorError
from utils import clean_input_lines, is_valid_vm_file

def main():

    args = sys.argv

    if (len(args) != 2):
        print('Usage: python VMTranslator.py')
        sys.exit(1)

    try:
        input_file_name = args[1]

        is_valid_vm_file(input_file_name)

        vm_commands: list[str] = []
        with open(input_file_name, 'r') as vm_file:
            lines = vm_file.readlines()
            vm_commands = clean_input_lines(lines)

        # TODO:
        # translate into Hack ASM
        # write output to .asm file of the same name

    except VMTranslatorError as error:
        print(f'Error: {error}')
        sys.exit(1)

    except Exception:
        print(traceback.format_exc())
        sys.exit(2)

if __name__ == '__main__':
    main()
