import pytest
import math
from src.factorial_and_fibo import _check_n, factorial, factorial_recursive, fibo, fibo_recursive


@pytest.mark.parametrize(
    'n, should_raise',
    [
        (0, False),
        (1, False),
        (5, False),
        (10, False),
        (-1, True),
        (-10, True),
        (1.5, True),
        ('3', True),
        (True, True),
        (False, True),
    ],
)
def test_check_n(n, should_raise):
    if should_raise:
        with pytest.raises(ValueError):
            _check_n(n)
    else:
        _check_n(n)


@pytest.mark.parametrize('n', [0, 1, 2, 3, 5, 7, 10, 15, 20, 100, 1000, 10000])
def test_factorial(n):
    assert factorial(n) == math.factorial(n)


@pytest.mark.parametrize('n', [0, 1, 2, 3, 5, 7, 10, 15, 20, 100, 900])
def test_factorial_recursive(n):
    assert factorial_recursive(n) == math.factorial(n)


@pytest.mark.parametrize(
    'n, res',
    [
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 2),
        (4, 3),
        (5, 5),
        (6, 8),
        (7, 13),
        (8, 21),
        (9, 34),
        (10, 55),
        (15, 610),
        (20, 6765),
    ],
)
def test_fibo(n, res):
    assert fibo(n) == res


@pytest.mark.parametrize(
    'n, res',
    [
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 2),
        (4, 3),
        (5, 5),
        (6, 8),
        (7, 13),
        (8, 21),
        (9, 34),
        (10, 55),
        (15, 610),
        (20, 6765),
    ],
)
def test_fibo_recursive(n, res):
    assert fibo_recursive(n) == res
