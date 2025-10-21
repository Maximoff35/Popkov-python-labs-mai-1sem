from src import tokenizer
from src import errors
import pytest


@pytest.mark.parametrize(
    "virazhenie, tokens",
    [
        ("1+2", [('NUM', 1), ('OP', '+'), ('NUM', 2)]),
        ("  1\t+\n2  ", [('NUM', 1), ('OP', '+'), ('NUM', 2)]),
        ("(3-4)", [('LP', '('), ('NUM', 3), ('OP', '-'), ('NUM', 4), ('RP', ')')]),
        ("1+2-3*4/5%6",
         [('NUM', 1), ('OP', '+'), ('NUM', 2), ('OP', '-'), ('NUM', 3), ('OP', '*'), ('NUM', 4), ('OP', '/'),
          ('NUM', 5), ('OP', '%'), ('NUM', 6)]),
        ("10.5+2.0", [('NUM', 10.5), ('OP', '+'), ('NUM', 2.0)]),
        ("0.0", [('NUM', 0.0)]),
        ("007+08", [('NUM', 7), ('OP', '+'), ('NUM', 8)]),
        ("2**3", [('NUM', 2), ('OP', '**'), ('NUM', 3)]),
        ("7//3", [('NUM', 7), ('OP', '//'), ('NUM', 3)]),
        ("12 // 5 ** 2", [('NUM', 12), ('OP', '//'), ('NUM', 5), ('OP', '**'), ('NUM', 2)]),
        ("-5", [('OP', '-'), ('NUM', 5)]),
        ("(-3)", [('LP', '('), ('OP', '-'), ('NUM', 3), ('RP', ')')]),
        (")", [('RP', ')')]),
        ("2***3", [('NUM', 2), ('OP', '**'), ('OP', '*'), ('NUM', 3)]),
        ("2////3", [('NUM', 2), ('OP', '//'), ('OP', '//'), ('NUM', 3)]),
        ("     \n\n  \t\t   ", []),
        ("((1+2)", [('LP', '('), ('LP', '('), ('NUM', 1), ('OP', '+'), ('NUM', 2), ('RP', ')')]),

    ]
)
def test_tokenize_good(virazhenie, tokens):
    assert tokenizer.tokenize(virazhenie) == tokens


@pytest.mark.parametrize(
    "virazhenie, oshibka",
    [
        ("1+a", "a"),
        ("e10", "e"),
        ("1e3", "e"),
        (".5", "."),
        ("1.", "."),
        ("1,2", ","),
        ("2@3", "@"),
        ("$5", "$"),
    ]
)
def test_tokenize_oshibki(virazhenie, oshibka):
    with pytest.raises(errors.TokenizeError) as ei:
        tokenizer.tokenize(virazhenie)
    assert oshibka in str(ei.value)


def test_tokenize_types():
    t = tokenizer.tokenize("38 + 31.15")
    assert t == [('NUM', 38), ('OP', '+'), ('NUM', 31.15)]
    assert isinstance(t[0][1], int)
    assert isinstance(t[1][1], str)
    assert isinstance(t[2][1], float)
