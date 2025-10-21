class BaseInstruction():

    def __init__(self, line_num, parts):
        pass

    def to_asm(self) -> list[str]:
        return []

# arithmetic/logical instructions

class AddInstruction(BaseInstruction):
    pass

class SubInstruction(BaseInstruction):
    pass

class NegInstruction(BaseInstruction):
    pass

class EqInstruction(BaseInstruction):
    pass

class GtInstruction(BaseInstruction):
    pass

class LtInstruction(BaseInstruction):
    pass

class AndInstruction(BaseInstruction):
    pass

class OrInstruction(BaseInstruction):
    pass

class NotInstruction(BaseInstruction):
    pass

# memory instructions

class PushInstruction(BaseInstruction):
    pass

class PopInstruction(BaseInstruction):
    pass