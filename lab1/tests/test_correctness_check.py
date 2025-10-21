from src import parser
from src import errors
import pytest


@pytest.mark.parametrize(
    "tokens",
    [
        [('NUM', 1)],
        [('OP', 'NEG'), ('NUM', 5)],
        [('NUM', 2), ('OP', '+'), ('NUM', 3)],
        [('LP', '('), ('NUM', 1), ('OP', '+'), ('NUM', 2), ('RP', ')')],
        [('NUM', 2), ('OP', '+'), ('OP', 'NEG'), ('NUM', 3)],
        [('LP', '('), ('LP', '('), ('NUM', 1), ('RP', ')'), ('OP', '+'), ('NUM', 2), ('RP', ')')],
    ]
)
def test_correctness_check_good(tokens):
    parser.correctness_check(tokens)


@pytest.mark.parametrize(
    "tokens",
    [
        [('OP', '+'), ('NUM', 1)],
        [('RP', ')'), ('NUM', 1)],
        [],
        [('NUM', 1), ('NUM', 2)],
        [('RP', ')'), ('NUM', 2)],
        [('NUM', 1), ('OP', '+'), ('OP', '*'), ('NUM', 2)],
        [('LP', '('), ('OP', '-'), ('NUM', 1)],
        [('NUM', 1), ('LP', '('), ('NUM', 2), ('RP', ')')],
        [('LP', '('), ('NUM', 1), ('RP', ')'), ('LP', '('), ('NUM', 2), ('RP', ')')],
        [('LP', '('), ('RP', ')')],
        [('NUM', 1), ('OP', '+'), ('RP', ')')],
        [('NUM', 1), ('OP', '+')],
        [('NUM', 1), ('OP', '+'), ('LP', '(')],
        [('NUM', 1), ('OP', '+'), ('NUM', 2), ('RP', ')')],
        [('LP', '('), ('NUM', 1), ('OP', '+'), ('NUM', 2)]
    ]
)
def test_correctness_check_oshibki(tokens):
    with pytest.raises(errors.ParseError):
        parser.correctness_check([])
