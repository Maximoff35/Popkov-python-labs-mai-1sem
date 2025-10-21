import pytest
from src import calculator
from src import errors


@pytest.mark.parametrize(
    ("virazhenie", "result"),
    [
        ("2+2", 4),
        ("3*(2+1)", 9),
        ("-3+5", 2),
        ("(-3)+(+5)", 2),
        ("(2**3)**2", 64),
        ("2**3**2", 512),
        ("8/4", 2),
        ("10/4", 2.5),
        ("7//3", 2),
        ("7%3", 1),
        ("2*-3", -6),
        ("   3   +   \n -   2  \t ", 1),
        ("2.5*2", 5.0),
        ("2+3*4", 14),
        ("((2))", 2),
        ("2--3", 5),
        ("-2**2", 4),
    ],
)
def test_calc_good(virazhenie, result):
    assert calculator.calc(virazhenie) == result


def test_calc_TokenizeError():
    with pytest.raises(errors.TokenizeError):
        calculator.calc("2 ? 3")


def test_calc_ParseError():
    with pytest.raises(errors.ParseError):
        calculator.calc("2+")


def test_calc_EvalError():
    with pytest.raises(errors.EvalError):
        calculator.calc("1/0")
