import re

TOKEN_RE = re.compile(r"(?P<NUM>\d+\.\d+|\d+)|(?P<OP>\*\*|//|[+\-*/%])|(?P<LP>\()|(?P<RP>\))|(?P<WS>\s+)|(?P<MIS>.)")

# чем больше, тем сильнее
PRIORITY = {
    '**': 3,
    'NEG': 4,  # унарный минус
    '*': 2, '//': 2, '%': 2, '/': 2,
    '+': 1, '-': 1
}


# левая или правая ассоциативность
def left(a, b):
    return a <= b


def right(a, b):
    return a < b


ASSOCIATIVITY = {
    '**': right,
    'NEG': right,
    '*': left, '//': left, '%': left, '/': left,
    '+': left, '-': left
}

UNARY_LEFT = (None, 'OP', 'LP')
