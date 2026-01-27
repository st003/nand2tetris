class JackCompilerError(Exception):
    """Base exception for errors handled by the JackCompiler."""
    def __str__(self):
        return f'Error - {self.args[0]}'

class CompilationEngineError(JackCompilerError):
    """Exception for errors handled by the CompilationEngine."""

    def __init__(self, tokenizer, message):
        self.tokenizer = tokenizer
        super().__init__(message)

    def __str__(self):
        return f'Error - line {self.tokenizer.line_num} - {self.args[0]}'

class JackTokenizerError(JackCompilerError):
    """Exception for errors handled by the JackTokenizer."""
    pass

class SymbolTableError(JackCompilerError):
    """Exception for errors handled by the SymbolTable."""
    pass
