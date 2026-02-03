from exceptions import SymbolTableError

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

    def varExists(self, name):
        """Checks if a variable of the given name exists."""
        if self._class_scope.get(name):
            return True
        elif self._subroutine_scope.get(name):
            return True
        else:
            return False

    def VarCount(self, kind):
        """For the current scope, returns the count of the kinds of symbols."""
        if kind == 'static':
            return self._static_count
        elif kind == 'field':
            return self._field_count
        elif kind == 'argument':
            return self._argument_count
        elif kind == 'local':
            return self._local_count
        else:
            raise SymbolTableError(f"SymbolTable.VarCount() - '{kind}' is not a valid symbol kind")

    def KindOf(self, name):
        """Returns the kind of the named symbol."""
        if self._class_scope.get(name):
            return self._class_scope[name]['kind']
        elif self._subroutine_scope.get(name):
            return self._subroutine_scope[name]['kind']
        else:
            raise SymbolTableError(f"SymbolTable.KindOf() - Symbol with name '{name}' does not exist")

    def TypeOf(self, name):
        """Returns the type of the named symbol."""
        if self._class_scope.get(name):
            return self._class_scope[name]['type']
        elif self._subroutine_scope.get(name):
            return self._subroutine_scope[name]['type']
        else:
            raise SymbolTableError(f"SymbolTable.TypeOf() - Symbol with name '{name}' does not exist")

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
        print('\nclass')
        self.pretty_print_table(self._class_scope)

    def print_subroutine_table(self, subroutine_type, subroutine_name):
        """Prints out the subroutine-level symbol table for debugging."""
        print(f'\n{subroutine_type}: {subroutine_name}')
        self.pretty_print_table(self._subroutine_scope)

    @staticmethod
    def pretty_print_table(table):
        """Pretty printer for tables."""

        if len(table) == 0:
            print('No symbols')
            return

        maxVarLen = 0
        maxTypeLen = 0
        maxKindLen = 0

        for k, v in table.items():
            maxVarLen = len(k) if (len(k) > maxVarLen) else maxVarLen
            maxTypeLen = len(v['type']) if (len(v['type']) > maxTypeLen) else maxTypeLen
            maxKindLen = len(v['kind']) if (len(v['kind']) > maxKindLen) else maxKindLen

        for k, v in table.items():
            varName = k + (' ' * (maxVarLen - len(k)))
            typeVal = v['type'] + (' ' * (maxTypeLen - len(v['type'])))
            kind = v['kind'] + (' ' * (maxKindLen - len(v['kind'])))
            print(f'|{varName}|{typeVal}|{kind}|{v['index']}|')
