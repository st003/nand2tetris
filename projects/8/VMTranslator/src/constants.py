import instructions as ins

ARITHMETIC_LOGICAL_INS_MAP = {
    'add': ins.AddInstruction,
    'sub': ins.SubInstruction,
    'neg': ins.NegInstruction,
    'eq': ins.EqInstruction,
    'gt': ins.GtInstruction,
    'lt': ins.LtInstruction,
    'and': ins.AndInstruction,
    'or': ins.OrInstruction,
    'not': ins.NotInstruction
}

BRANCH_INS_MAP = {
    'goto': ins.GotoInstruction,
    'if-goto': ins.IfGotoInstruction,
    'label': ins.LabelInstruction
}

MEMORY_INS_MAP = {
    'push': ins.PushInstruction,
    'pop': ins.PopInstruction
}

FUNCTION_INS_MAP = {
    'call': ins.CallInstruction,
    'function': ins.FunctionInstruction,
    'return': ins.ReturnInstruction
}

MEMORY_SEGMENTS = {
    'local',
    'argument',
    'this',
    'that',
    'constant',
    'static',
    'pointer',
    'temp'
}
