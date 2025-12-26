class JackAnalyzerError(Exception):
    """Base exception for errors handled by the JackAnalyzer."""
    pass

class JackTokenizerError(JackAnalyzerError):
    """Base exception for errors handled by the JackTokenizer."""
    pass
