from __future__ import annotations
from src.models import Book


class BookCollection:
    """
    Пользовательская списковая коллекция книг.

    Хранит объекты класса Book и его подклассов.
    Поддерживает длину, итерацию, индексацию, срезы,
    добавление и удаление книг.
    """

    def __init__(self, books: list[Book] | None = None) -> None:
        """
        Инициализация коллекции. Ничего не возвращает.
        :param books: Список объектов Book или None для создания пустой коллекции
        """
        self._books = []
        if books is None:
            return
        if type(books) is not list:
            raise ValueError('Коллекцию можно создать только из списка книг.')
        for book in books:
            self.add_book(book)

    def add_book(self, book: Book) -> None:
        """
        Добавляет книгу в коллекцию. Ничего не возвращает.
        :param book: Объект класса Book или его подклассов
        """
        if not isinstance(book, Book):
            raise ValueError('Коллекция может состоять только из объектов типа Book.')
        isbn = book.isbn
        if self.contain_isbn(isbn):
            self.remove_book_by_isbn(isbn)
        self._books.append(book)

    def remove_book_by_isbn(self, isbn: str) -> None:
        """
        Удаляет книгу по её ISBN. Ничего не возвращает.
        :param isbn: Строка с ISBN книги, которую требуется удалить
        :raises KeyError: Если книга с указанным ISBN не найдена
        """
        if type(isbn) is not str or isbn.strip() == '':
            raise ValueError('В поле "isbn" ожидается непустая строка.')
        isbn = isbn.strip()
        for i in range(len(self)):
            if self._books[i].isbn == isbn:
                self._books = self._books[:i] + self._books[i + 1:]
                return
        raise KeyError('ISBN не найден в коллекции.')

    def contain_isbn(self, isbn: str) -> bool:
        """
        Проверяет, содержится ли в коллекции книга с указанным ISBN
        :param isbn: Строка с ISBN книги
        :return: True, если книга с указанным ISBN есть в коллекции, иначе, False
        """
        if type(isbn) is not str or isbn.strip() == '':
            raise ValueError('В поле "isbn" ожидается непустая строка.')
        isbn = isbn.strip()
        return any(book.isbn == isbn for book in self)

    def __len__(self) -> int:
        """
        Возвращает количество книг в коллекции.
        :return: Целое число — размер коллекции
        """
        return len(self._books)

    def __iter__(self):
        """
        Возвращает итератор по книгам в коллекции.
        :return: Итератор по объектам Book
        """
        return iter(self._books)

    def __getitem__(self, item: int | slice) -> Book | "BookCollection":
        """
        Возвращает книгу по индексу или подколлекцию по срезу.
        :param item: Индекс (int) или срез (slice)
        :return: Объект Book или новая BookCollection
        """
        if type(item) is int:
            return self._books[item]
        if type(item) is slice:
            return BookCollection(self._books[item])
        raise ValueError('В поле "item" ожидается целое число или срез.')

    def __contains__(self, other: Book) -> bool:  # ПОДУМАТЬ
        """
        Проверяет наличие книги в коллекции.
        :param other: Объект класса Book или его подклассов
        :return: True, если книга найдена, иначе False
        """
        if not isinstance(other, Book):
            raise ValueError('В коллекции можно искать только книги класса Book или его подклассов.')
        return other in self._books


class IndexDict:
    """
    Пользовательская словарная коллекция индексов книг.

    Хранит три индекса: по ISBN, по автору и по году издания.
    Обеспечивает быстрый поиск книг и поддерживает
    согласованность данных при добавлении и удалении.
    """

    def __init__(self, books: BookCollection | None = None):
        """
        Инициализация структуры индексов. Ничего не возвращает.
        :param books: Коллекция BookCollection или None.
                      Если указана, индекс заполняется её книгами.
        """
        self._by_isbn = {}
        self._by_author = {}
        self._by_year = {}
        if books is None:
            return
        for book in books:
            self.add_book(book)

    def add_book(self, book: Book) -> None:
        """
        Добавляет книгу во все индексы. Ничего не возвращает.
        :param book: Объект класса Book или его подклассов
        :raises ValueError: Если передан не объект класса Book
        """
        if not isinstance(book, Book):
            raise ValueError('Индекс может состоять только из объектов типа Book.')
        isbn = book.isbn
        author = book.author
        year = book.year
        if isbn in self._by_isbn:
            self.remove_book_by_isbn(isbn)
        self._by_isbn[isbn] = book
        if author not in self._by_author:
            self._by_author[author] = [book]
        else:
            self._by_author[author].append(book)
        if year not in self._by_year:
            self._by_year[year] = [book]
        else:
            self._by_year[year].append(book)

    def remove_book(self, book: Book) -> None:
        """
        Удаляет книгу из всех индексов по объекту книги.
        :param book: Объект класса Book, который требуется удалить
        :raises ValueError: Если передан не объект Book
        :raises KeyError: Если книги нет в индексе
        """
        if not isinstance(book, Book):
            raise ValueError('Индекс состоит только из объектов типа Book.')
        if book.isbn not in self._by_isbn or self._by_isbn[book.isbn] != book:
            raise KeyError('Неизвестная книга.')
        self.remove_book_by_isbn(book.isbn)

    def remove_book_by_isbn(self, isbn: str) -> None:
        """
        Удаляет книгу из всех индексов по её ISBN.
        :param isbn: Строка с ISBN удаляемой книги
        :raises ValueError: Если ISBN не является непустой строкой
        :raises KeyError: Если книга с таким ISBN отсутствует в индексе
        """
        if type(isbn) is not str or isbn.strip() == '':
            raise ValueError('В поле "isbn" ожидается непустая строка.')
        isbn = isbn.strip()
        if isbn not in self._by_isbn:
            raise KeyError('Неизвестная книга.')
        old_book = self._by_isbn[isbn]
        del self._by_isbn[isbn]
        self._by_author[old_book.author].remove(old_book)
        if not self._by_author[old_book.author]:
            del self._by_author[old_book.author]
        self._by_year[old_book.year].remove(old_book)
        if not self._by_year[old_book.year]:
            del self._by_year[old_book.year]

    def get_by_isbn(self, isbn: str) -> Book:
        """
        Возвращает книгу по её ISBN.
        :param isbn: Строка с ISBN книги
        :return: Объект Book
        :raises ValueError: Если ISBN некорректен
        :raises KeyError: Если книги с таким ISBN нет в индексе
        """
        if type(isbn) is not str or isbn.strip() == '':
            raise ValueError('В поле "isbn" ожидается непустая строка.')
        isbn = isbn.strip()
        if isbn not in self._by_isbn:
            raise KeyError('Неизвестная книга.')
        return self._by_isbn[isbn]

    def get_by_author(self, author: str) -> list[Book]:
        """
        Возвращает список книг указанного автора.
        :param author: Строка — имя автора
        :return: Список объектов Book данного автора
        :raises ValueError: Если автор указан некорректно
        :raises KeyError: Если автор отсутствует в индексе
        """
        if type(author) is not str or author.strip() == '':
            raise ValueError('В поле "author" ожидается непустая строка.')
        author = author.strip()
        if author not in self._by_author:
            raise KeyError('Неизвестный автор.')
        return self._by_author[author]

    def get_by_year(self, year: int) -> list[Book]:
        """
        Возвращает список книг, изданных в указанном году.
        :param year: Целое число — год издания
        :return: Список объектов Book
        :raises ValueError: Если год некорректен
        :raises KeyError: Если в этом году нет ни одной книги
        """
        if type(year) is not int:
            raise ValueError('В поле "year" ожидается целое число.')
        if not (0 <= year <= 2026):
            raise ValueError('Год должен быть от 0 до 2026.')
        if year not in self._by_year:
            raise KeyError('Неизвестный год.')
        return self._by_year[year]

    def __len__(self):
        """
        Возвращает количество уникальных ISBN в индексе.
        :return: Целое число — количество книг в индексе
        """
        return len(self._by_isbn)

    def __iter__(self):
        """
        Возвращает итератор по всем книгам в индексе.
        :return: Итератор по объектам Book
        """
        return iter(self._by_isbn.values())

    def __getitem__(self, isbn: str) -> Book:
        """
        Позволяет получить книгу по ISBN через синтаксис index[isbn].
        :param isbn: Строка с ISBN книги
        :return: Объект Book
        :raises ValueError: Если ISBN некорректен
        :raises KeyError: Если книги с таким ISBN нет в индексе
        """
        if type(isbn) is not str or isbn.strip() == '':
            raise ValueError('В поле "isbn" ожидается непустая строка.')
        isbn = isbn.strip()
        if isbn not in self._by_isbn:
            raise KeyError('Неизвестная книга.')
        return self._by_isbn[isbn]

    def __setitem__(self, isbn: str, book: Book) -> None:
        """
        Позволяет добавить книгу через синтаксис index[isbn] = book.
        :param isbn: Строка с ISBN
        :param book: Объект Book, который требуется добавить
        :raises ValueError: Если ISBN некорректен или не совпадает с ISBN книги
        """
        if type(isbn) is not str or isbn.strip() == '':
            raise ValueError('В поле "isbn" ожидается непустая строка.')
        isbn = isbn.strip()
        if book.isbn != isbn:
            raise ValueError('ISBN не соответствует этой книге.')
        self.add_book(book)

    def __contains__(self, isbn: str) -> bool:
        """
        Проверяет наличие книги в индексе.
        :param isbn: Строка с ISBN
        :return: True, если книга найдена, иначе False
        """
        if type(isbn) is not str or isbn.strip() == '':
            raise ValueError('В поле "isbn" ожидается непустая строка.')
        isbn = isbn.strip()
        return isbn in self._by_isbn
