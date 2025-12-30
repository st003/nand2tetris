import tokens as T

KEYWORDS = {
    'class',
    'constructor',
    'function',
    'method',
    'field',
    'static',
    'var',
    'int',
    'char',
    'boolean',
    'void',
    'true',
    'false',
    'null',
    'this',
    'let',
    'do',
    'if',
    'else',
    'while',
    'return'
}

SYMBOLS = {
    '(',
    ')',
    '{',
    '}',
    '[',
    ']',
    '.',
    ',',
    ';',
    '+',
    '-',
    '*',
    '/',
    '&',
    '|',
    '<',
    '>',
    '=',
    '~'
}

def get_token(identifier):

    if identifier in KEYWORDS:
        return T.KeywordToken(identifier)

    if identifier in SYMBOLS:
        return T.SymbolToken(identifier)

    return T.BaseToken(identifier)
