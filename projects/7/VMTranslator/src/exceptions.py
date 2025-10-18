class VMTranslatorError(Exception):
    """Base exception for errors handled by the VM Translator."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
