def _check_int_array(array):
    """
    Функция для вызова ValueError, если array не является списком целых чисел list[int]
    :param array: Список целых чисел
    :return: Ничего не возвращает
    """
    if type(array) is not list or any(type(x) is not int for x in array):
        raise ValueError('Аргумент не является списком целых чисел.')


def _check_int_nonneg_array(array):
    """
    Функция для вызова ValueError, если array не является списком целых неотрицательных чисел list[int]
    :param array: Список целых неотрицательных чисел
    :return: Ничего не возвращает
    """
    if type(array) is not list or any(type(x) is not int or x < 0 for x in array):
        raise ValueError('Аргумент не является списком целых неотрицательных чисел.')


def selection_sort(array: list[int]) -> list[int]:
    """
    Сортировка выбором.
    :param array: Список целых чисел
    :return: Список целых чисел, отсортированных по возрастанию
    """
    _check_int_array(array)
    for i in range(len(array)):
        for j in range(i + 1, len(array)):
            if array[i] > array[j]:
                array[i], array[j] = array[j], array[i]
    return array


def bubble_sort(array: list[int]) -> list[int]:
    """
    Сортировка пузырьком.
    :param array: Список целых чисел
    :return: Список целых чисел, отсортированных по возрастанию
    """
    _check_int_array(array)
    for i in range(len(array) - 1):
        f = False
        for j in range(len(array) - 1 - i):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                f = True
        if not f:
            break
    return array


def quick_sort(array: list[int], correctness=False) -> list[int]:
    """
    Рекурсивный алгоритм QuickSort, сортирует по возрастанию список целых чисел
    :param array: Список целых чисел
    :return: Список целых чисел, отсортированных по возрастанию
    """
    if not correctness:
        _check_int_array(array)
    if len(array) <= 1:
        return array
    mid_elem = array[len(array) // 2]
    left, mid, right = [], [], []
    for i in range(len(array)):
        if array[i] < mid_elem:
            left.append(array[i])
        elif array[i] > mid_elem:
            right.append(array[i])
        else:
            mid.append(array[i])

    return quick_sort(left, True) + mid + quick_sort(right, True)


def counting_sort(array: list[int]) -> list[int]:
    """
    Алгоритм CountingSort, сортирует по возрастанию список целых чисел
    :param array: Список целых чисел
    :return: Список целых чисел, отсортированных по возрастанию
    """
    _check_int_array(array)

    if not array:
        return []

    min_val, max_val = float('inf'), float('-inf')
    for x in array:
        min_val = min(min_val, x)
        max_val = max(max_val, x)

    cnts = [0] * (max_val - min_val + 1)
    for x in array:
        cnts[x - min_val] += 1

    res = []
    for i in range(max_val - min_val + 1):
        res += [i + min_val] * cnts[i]
    return res


def radix_sort(array: list[int], base: int = 10) -> list[int]:
    """
    Алгоритм RadixSort, сортирует по возрастанию список целых НЕОТРИЦАТЕЛЬНЫХ чисел
    :param array: Список целых неотрицательных чисел
    :return: Список целых неотрицательных чисел, отсортированных по возрастанию
    """
    _check_int_nonneg_array(array)

    if not array:
        return []

    if type(base) is not int or base <= 1:
        raise ValueError('Основание системы счисления должно быть >= 2.')

    cnt_digits = 0
    n = max(array)
    while n > 0:
        cnt_digits += 1
        n //= base

    for i in range(cnt_digits):
        buckets = [[] for _ in range(base)]
        for x in array:
            digit = (x // (base ** i)) % base
            buckets[digit].append(x)
        array = []
        for j in range(base):
            array += buckets[j]

    return array


def bucket_sort(array: list[float], buckets: int | None = None) -> list[float]:
    """
    Алгоритм BucketSort, сортирует по возрастанию список вещественных чисел в диапазоне [0; 1).
    :param array: Список вещественных чисел в диапазоне [0; 1)
    :param buckets: Количество используемых для сортировки корзин (целое число >= 1)
    :return: Список вещественных чисел в диапазоне [0; 1), отсортированных по возрастанию
    """
    if type(array) is not list or any((type(x) is not float and type(x) is not int) or x < 0 or x >= 1 for x in array):
        raise ValueError('Передан некорректный массив. Ожидается массив вещественных чисел в диапазоне [0; 1).')

    if buckets is not None and (type(buckets) is not int or buckets < 1):
        raise ValueError('Передано некорректное количество корзин. Ожидается целое число >= 1.')

    if not array:
        return []

    if buckets is None:
        buckets = len(array)

    buckets_list = [[] for _ in range(buckets)]
    for x in array:
        index = min(buckets - 1, int(x * buckets))
        buckets_list[index].append(x)

    res = []
    for lst in buckets_list:
        res += _selection_sort(lst)
    return res


def _selection_sort(array: list[float]) -> list[float]:
    """
    Сортировка выбором.
    :param array: Список вещественных чисел в диапазоне [0; 1)
    :return: Список вещественных чисел в диапазоне [0; 1), отсортированных по возрастанию
    """
    for i in range(len(array)):
        for j in range(i + 1, len(array)):
            if array[i] > array[j]:
                array[i], array[j] = array[j], array[i]
    return array


def heap_sort(array: list[int]) -> list[int]:
    """
    Алгоритм HeapSort, сортирует по возрастанию список целых чисел
    :param array: Список целых чисел
    :return: Список целых чисел, отсортированных по возрастанию
    """
    _check_int_array(array)
    n = len(array)
    if n <= 1:
        return array

    def _heapify(arr: list[int], heap_size: int, i: int) -> None:
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < heap_size and arr[left] > arr[largest]:
            largest = left
        if right < heap_size and arr[right] > arr[largest]:
            largest = right

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            _heapify(arr, heap_size, largest)

    for i in range(n // 2 - 1, -1, -1):
        _heapify(array, n, i)

    for end in range(n - 1, 0, -1):
        array[0], array[end] = array[end], array[0]
        _heapify(array, end, 0)

    return array

