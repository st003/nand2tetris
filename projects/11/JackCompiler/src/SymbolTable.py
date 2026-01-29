from exceptions import SymbolTableError

# TODO: api implementation def found at: 5.10 @10:00

class SymbolTable():
    """Class for managing class and subroutine symbol tables."""

    def __init__(self):
        """Initializes the class and subroutine symbol table."""
        self._class_scope = {}
        self._static_count = 0
        self._field_count = 0

        self._subroutine_scope = {}
        self._argument_count = 0
        self._local_count = 0

    def startSubroutine(self):
        """Resets the subroutine symbol table."""
        self._subroutine_scope = {}
        self._argument_count = 0
        self._local_count = 0

    def define(self, name, type, kind):
        """Inserts a new entry into the correct symbol table."""

        if kind == 'static':
            self._class_scope[name] = {
                'type': type,
                'kind': kind,
                'index': self._static_count
            }
            self._static_count += 1

        elif kind == 'field':
            self._class_scope[name] = {
                'type': type,
                'kind': kind,
                'index': self._field_count
            }
            self._field_count += 1

        elif kind == 'argument':
            self._subroutine_scope[name] = {
                'type': type,
                'kind': kind,
                'index': self._argument_count
            }
            self._argument_count += 1

        elif kind == 'local':
            self._subroutine_scope[name] = {
                'type': type,
                'kind': kind,
                'index': self._local_count
            }
            self._local_count += 1

        else:
            raise SymbolTableError(f"SymbolTable.define() - Invalid symbol kind: '{kind}'")

    def VarCount(self, kind):
        # TODO: implement
        return 0

    def KindOf(self, name):
        """Returns the kind of the named symbol."""
        if self._class_scope.get(name):
            return self._class_scope[name]['kind']
        elif self._subroutine_scope.get(name):
            return self._subroutine_scope[name]['kind']
        else:
            raise SymbolTableError(f"SymbolTable.KindOf() - Symbol with name '{name}' does not exist")

    def TypeOf(self, name):
        # TODO: implement
        pass

    def IndexOf(self, name):
        """Returns the index of the named symbol."""
        if self._class_scope.get(name):
            return self._class_scope[name]['index']
        elif self._subroutine_scope.get(name):
            return self._subroutine_scope[name]['index']
        else:
            raise SymbolTableError(f"SymbolTable.IndexOf() - Symbol with name '{name}' does not exist")

    def print_class_table(self, class_name):
        """Prints out the class-level symbol table for debugging."""
        print(f"\nDebug - Symbol Tables for '{class_name}'")
        print('\nClass')
        print(self._class_scope)

    def print_subroutine_table(self, subroutine_name):
        """Prints out the subroutine-level symbol table for debugging."""
        print(f'\n{subroutine_name}')
        print(self._subroutine_scope)