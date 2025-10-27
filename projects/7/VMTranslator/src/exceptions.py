class VMTranslatorError(Exception):
    """Base exception for errors handled by the VM Translator."""
    pass

class ParseError(VMTranslatorError):
    """Errors thrown by the parser"""
    pass

class TranslationError(VMTranslatorError):
    """Errors thrown by the translator"""
    pass
