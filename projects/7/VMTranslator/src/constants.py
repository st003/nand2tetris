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

MEMORY_INS_MAP = {
    'push': ins.PushInstruction,
    'pop': ins.PopInstruction
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
