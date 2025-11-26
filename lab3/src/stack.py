class Stack:
    """
    Стек с поддержкой операции min() за O(1).
    Каждый элемент хранится как кортеж:
    (значение, доступен_минимум, текущий_минимум_до_него_вкл).
    """

    def __init__(self, lst: list | None = None) -> None:
        """
        Инициализация.
        :param lst: начальный список значений для добавления в стек
        """
        self._data = []
        if lst is None:
            return
        if type(lst) is not list:
            raise ValueError('Ожидался список.')
        for x in lst:
            self.push(x)

    def push(self, x: object) -> None:
        """
        Добавляет элемент в стек.
        :param x: значение, добавляемое в стек
        :return: ничего не возвращает
        """
        if len(self) == 0:
            if type(x) is int or type(x) is float:
                self._data.append((x, True, x))
            else:
                self._data.append((x, False, None))
        else:
            if self._data[-1][1] and (type(x) is int or type(x) is float):
                self._data.append((x, True, min(x, self._data[-1][2])))
            else:
                self._data.append((x, False, None))

    def is_empty(self) -> bool:
        """
        Проверяет, пуст ли стек
        :return: bool: True, если стек пуст, иначе False.
        """
        return len(self) == 0

    def __len__(self) -> int:
        """
        Возвращает количество элементов в стеке.
        :return: длина стека
        """
        return len(self._data)

    def pop(self) -> object:
        """
        Удаляет и возвращает верхний элемент стека.
        :return: значение верхнего элемента
        """
        if self.is_empty():
            raise IndexError('Стек пустой.')
        return self._data.pop()[0]

    def peek(self) -> object:
        """
        Возвращает верхний элемент стека без удаления
        :return: значение верхнего элемента
        """
        if self.is_empty():
            raise IndexError('Стек пустой.')
        return self._data[-1][0]

    def min(self) -> int | float:
        """
        Возвращает минимальное число в стеке за O(1).
        :return: минимальное значение среди числовых элементов.
        """
        if not self._data[-1][1]:
            raise ValueError('min поддерживается только для чисел.')
        if self.is_empty():
            raise IndexError('Стек пустой.')
        return self._data[-1][2]
