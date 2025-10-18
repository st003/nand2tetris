import sys
import traceback

from exceptions import VMTranslatorError
from utils import is_valid_vm_file

def main():

    args = sys.argv

    if (len(args) != 2):
        print('Usage: python VMTranslator.py')
        sys.exit(1)

    try:
        input_file_name = args[1]

        is_valid_vm_file(input_file_name)

        # TODO:
        # load file into memory
        # parse input lines, removing comments & whitespace
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
