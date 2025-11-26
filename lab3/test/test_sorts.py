import pytest
from src.sorts import *
from random import randrange


def generate_array(n, min_value, max_value, func=lambda x: x, check_func=lambda x, y: True):
    if n == 0:
        return []
    array = [func(randrange(min_value, max_value))]
    for i in range(n - 1):
        a = func(randrange(min_value, max_value))
        while not check_func(array[-1], a):
            a = func(randrange(min_value, max_value))
        array.append(a)
    return array


def generate_cases_for_all_int():
    cases = [generate_array(100, -1000, 1000, check_func=lambda x, y: x <= y)]
    cases += [generate_array(100, -1000, 1000, check_func=lambda x, y: x >= y)]
    for n in [0, 1, 5, 10, 100, 1000]:
        cases += [generate_array(n, -1000, 1000)]
    return cases


def generate_cases_for_non_neg_int():
    cases = [generate_array(100, 0, 1000, check_func=lambda x, y: x <= y)]
    cases += [generate_array(100, 0, 1000, check_func=lambda x, y: x >= y)]
    for n in [0, 1, 5, 10, 100, 1000]:
        cases += [generate_array(n, 0, 1000)]
    return cases


def generate_cases_for_0_1():
    cases = [generate_array(100, 0, 99999, func=lambda x: x / 100000, check_func=lambda x, y: x <= y)]
    cases += [generate_array(100, 0, 99999, func=lambda x: x / 100000, check_func=lambda x, y: x >= y)]
    for n in [0, 1, 5, 10, 100, 1000]:
        cases += [generate_array(n, 0, 99999, func=lambda x: x / 100000)]
    return cases


def test_bubble_sort():
    cases = generate_cases_for_all_int()
    for case in cases:
        assert bubble_sort(case) == sorted(case)


def test_bubble_sort_errors():
    with pytest.raises(ValueError):
        bubble_sort(['abc', 'def', 'ghi'])
    with pytest.raises(ValueError):
        bubble_sort([1, 5, 'dsfjb', 123.45, -89.46])
    with pytest.raises(ValueError):
        bubble_sort(5)


def test_quick_sort():
    cases = generate_cases_for_all_int()
    for case in cases:
        assert quick_sort(case) == sorted(case)


def test_quick_sort_errors():
    with pytest.raises(ValueError):
        quick_sort(['abc', 'def', 'ghi'])
    with pytest.raises(ValueError):
        quick_sort([1, 5, 'dsfjb', 123.45, -89.46])
    with pytest.raises(ValueError):
        quick_sort(5)


def test_counting_sort():
    cases = generate_cases_for_all_int()
    for case in cases:
        assert counting_sort(case) == sorted(case)


def test_counting_sort_errors():
    with pytest.raises(ValueError):
        counting_sort(['abc', 'def', 'ghi'])
    with pytest.raises(ValueError):
        counting_sort([1, 5, 'dsfjb', 123.45, -89.46])
    with pytest.raises(ValueError):
        counting_sort(5)


def test_heap_sort():
    cases = generate_cases_for_all_int()
    for case in cases:
        assert heap_sort(case) == sorted(case)


def test_heap_sort_errors():
    with pytest.raises(ValueError):
        heap_sort(['abc', 'def', 'ghi'])
    with pytest.raises(ValueError):
        heap_sort([1, 5, 'dsfjb', 123.45, -89.46])
    with pytest.raises(ValueError):
        heap_sort(5)


def test_radix_sort():
    cases = generate_cases_for_non_neg_int()
    for case in cases:
        assert radix_sort(case) == sorted(case)


def test_radix_sort_errors():
    with pytest.raises(ValueError):
        radix_sort(['abc', 'def', 'ghi'])
    with pytest.raises(ValueError):
        radix_sort([1, 5, 'dsfjb', 123.45, -89.46])
    with pytest.raises(ValueError):
        radix_sort(5)
    with pytest.raises(ValueError):
        radix_sort([-5, -8, -51651, 0, 5465, 52])


def test_bucket_sort():
    cases = generate_cases_for_0_1()
    for case in cases:
        try:
            cnt = randrange(1, len(case) + 1)
        except:
            cnt = None
        assert bucket_sort(case, cnt) == sorted(case)


def test_bucket_sort_errors():
    with pytest.raises(ValueError):
        bucket_sort(['abc', 'def', 'ghi'])
    with pytest.raises(ValueError):
        bucket_sort([1, 5, 'dsfjb', 123.45, -89.46])
    with pytest.raises(ValueError):
        bucket_sort(5)
    with pytest.raises(ValueError):
        bucket_sort([-5, -8, -51651, 0, 5465, 52])