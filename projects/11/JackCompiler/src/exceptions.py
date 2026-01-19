class JackCompilerError(Exception):
    """Base exception for errors handled by the JackCompiler."""
    def __str__(self):
        return f'Error - {self.message}'

class CompilationEngineError(JackCompilerError):
    """Exception for errors handled by the CompilationEngine."""

    def __init__(self, tokenizer, message):
        self.tokenizer = tokenizer
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'Error - line {self.tokenizer.line_num} - {self.message}'

class JackTokenizerError(JackCompilerError):
    """Exception for errors handled by the JackTokenizer."""
    def __str__(self):
        return f'Error - {self.message}'

class SymbolTableError(JackCompilerError):
    """Exception for errors handled by the SymbolTable."""
    pass