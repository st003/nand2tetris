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

def get_token(value):

    if value in KEYWORDS:
        return T.KeywordToken(value)

    if value in SYMBOLS:
        return T.SymbolToken(value)

    return T.IdentifierToken(value)
