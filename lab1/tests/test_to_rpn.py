from src import parser
from src import errors
import pytest


@pytest.mark.parametrize(
    "tokens, rpn",
    [
        ([('NUM', 1), ('OP', '+'), ('NUM', 2)], [('NUM', 1), ('NUM', 2), ('OP', '+')]),
        ([('NUM', 2), ('OP', '+'), ('NUM', 3), ('OP', '*'), ('NUM', 4)],
         [('NUM', 2), ('NUM', 3), ('NUM', 4), ('OP', '*'), ('OP', '+')]),
        ([('LP', '('), ('NUM', 2), ('OP', '+'), ('NUM', 3), ('RP', ')'), ('OP', '*'), ('NUM', 4)],
         [('NUM', 2), ('NUM', 3), ('OP', '+'), ('NUM', 4), ('OP', '*')]),
        ([('OP', 'NEG'), ('NUM', 5)], [('NUM', 5), ('OP', 'NEG')]),
        ([('NUM', 2), ('OP', '**'), ('NUM', 3), ('OP', '**'), ('NUM', 2)],
         [('NUM', 2), ('NUM', 3), ('NUM', 2), ('OP', '**'), ('OP', '**')]),
        ([('NUM', 8), ('OP', '//'), ('NUM', 3)], [('NUM', 8), ('NUM', 3), ('OP', '//')]),
        ([('NUM', 12), ('OP', '//'), ('NUM', 5), ('OP', '**'), ('NUM', 2)],
         [('NUM', 12), ('NUM', 5), ('NUM', 2), ('OP', '**'), ('OP', '//')]),
        ([('LP', '('), ('NUM', 1), ('OP', '-'), ('NUM', 2), ('RP', ')'), ('OP', '-'), ('NUM', 3)],
         [('NUM', 1), ('NUM', 2), ('OP', '-'), ('NUM', 3), ('OP', '-')]),
        ([('NUM', 2), ('OP', '%'), ('NUM', 5), ('OP', '+'), ('NUM', 1)],
         [('NUM', 2), ('NUM', 5), ('OP', '%'), ('NUM', 1), ('OP', '+')])
    ]
)
def test_to_rpn_good(tokens, rpn):
    assert parser.to_rpn(tokens) == rpn


@pytest.mark.parametrize(
    "tokens",
    [
        ([('RP', ')')]),
        ([('LP', '('), ('NUM', 1)]),
        ([('UNK', '?')]),
        ([('LP', '('), ('NUM', 1), ('RP', ')'), ('RP', ')')])
    ]
)
def test_to_rpn_bad(tokens):
    with pytest.raises(errors.ParseError):
        parser.to_rpn(tokens)
