from src import errors
from src import evaluator
import pytest


@pytest.mark.parametrize(
    "rpn, result",
    [
        ([('NUM', 2), ('NUM', 3), ('OP', '+')], 5),
        ([('NUM', 2), ('NUM', 3), ('OP', '*')], 6),
        ([('NUM', 5), ('OP', 'NEG')], -5),
        ([('NUM', 2), ('NUM', 3), ('OP', '+'), ('NUM', 4), ('OP', '*')], 20),
        ([('NUM', 4), ('NUM', 2), ('OP', '/')], 2),
        ([('NUM', 7), ('NUM', 2), ('OP', '/')], 3.5),
        ([('NUM', 8), ('NUM', 3), ('OP', '//')], 2),
        ([('NUM', 7), ('NUM', 3), ('OP', '%')], 1),
        ([('NUM', 2), ('NUM', 3), ('OP', '**')], 8),
        ([('NUM', 2), ('NUM', 3), ('OP', 'NEG'), ('OP', '*')], -6),
        ([('NUM', 12), ('NUM', 5), ('OP', '//'), ('NUM', 2), ('OP', '**')], 4),
        ([('NUM', 10), ('NUM', 2), ('OP', '/'), ('NUM', 3), ('OP', '+')], 8),
        ([('NUM', 5.0), ('NUM', 2), ('OP', '//')], 2),
        ([('NUM', 9.0), ('NUM', 4.5), ('OP', '/')], 2)
    ]
)
def test_eval_rpn_good(rpn, result):
    assert evaluator.eval_rpn(rpn) == result


@pytest.mark.parametrize(
    "rpn",
    [
        ([('NUM', 1), ('NUM', 2)]),
        ([('NUM', 1), ('NUM', 0), ('OP', '/')]),
        ([('NUM', 1), ('NUM', 0), ('OP', '//')]),
        ([('NUM', 1), ('NUM', 0), ('OP', '%')]),
        ([('NUM', 5.5), ('NUM', 2), ('OP', '//')]),
        ([('NUM', 5), ('NUM', 2.5), ('OP', '//')]),
        ([('NUM', 5.5), ('NUM', 2), ('OP', '%')]),
        ([('NUM', 5), ('NUM', 2.5), ('OP', '%')])
    ]
)
def test_eval_rpn_bad(rpn):
    with pytest.raises(errors.EvalError):
        evaluator.eval_rpn(rpn)
