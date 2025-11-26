from functools import lru_cache


def _check_n(n: int) -> None:
    """
    Функция для вызова ValueError, если n не является целым неотрицательным числом
    :param n: Целое неотрицательное число
    :return: Ничего не возвращает
    """
    if type(n) is not int or n < 0:
        raise ValueError('Аргумент не является целым неотрицательным числом.')


def factorial(n: int) -> int:
    """
    Итеративно подсчитывает факториал числа
    :param n: Целое неотрицательное число
    :return: Результат - значение факториала
    """
    _check_n(n)
    res = 1
    for i in range(2, n + 1):
        res *= i
    return res


def factorial_recursive(n: int) -> int:
    """
    Рекурсивно подсчитывает факториал числа
    :param n: Целое неотрицательное число
    :return: Результат - значение факториала
    """
    _check_n(n)
    if n == 0:
        return 1
    else:
        return n * factorial_recursive(n - 1)


def fibo(n: int) -> int:
    """
    Итеративно подсчитывает n-ое число Фибоначчи. При n = 0 значение 0, при n = 1 значение 1.
    :param n: Целое неотрицательное число
    :return: Результат - значение n-го числа Фибоначчи
    """
    _check_n(n)
    a = 0
    b = 1
    for i in range(n):
        b, a = a + b, b
    return a


def fibo_recursive(n: int) -> int:
    """
    Рекурсивно подсчитывает n-ое число Фибоначчи. При n = 0 значение 0, при n = 1 значение 1.
    :param n: Целое неотрицательное число
    :return: Результат - значение n-го числа Фибоначчи
    """
    _check_n(n)
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return _fibo_recursive(n - 1) + _fibo_recursive(n - 2)


def _fibo_recursive(n: int) -> int:
    """
    Вспомогательная функция для подсчета n-го числа Фибоначчи без проверки корректности n
    :param n: Целое неотрицательное число
    :return: Результат - значение n-го числа Фибоначчи
    """
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return _fibo_recursive(n - 1) + _fibo_recursive(n - 2)