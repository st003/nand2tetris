class JackAnalyzerError(Exception):
    """Base exception for errors handled by the JackAnalyzer."""
    def __str__(self):
        return f'Error - {self.message}'

class CompilationEngineError(JackAnalyzerError):
    """Base exception for errors handled by the CompilationEngine."""

    def __init__(self, tokenizer, message):
        self.tokenizer = tokenizer
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'Error - line {self.tokenizer.line_num} - {self.message}'

class JackTokenizerError(JackAnalyzerError):
    """Base exception for errors handled by the JackTokenizer."""
    def __str__(self):
        return f'Error - {self.message}'
