from src.models import Book
from src.collections import BookCollection, IndexDict

class Library:
    """
    Класс библиотеки.

    Хранит коллекцию книг и индексы для быстрого поиска.
    Предоставляет методы добавления, удаления и поиска книг.
    """

    def __init__(self, books: BookCollection | None = None) -> None:
        """
        Инициализация библиотеки. Ничего не возвращает.
        :param books: Коллекция BookCollection или None для создания пустой библиотеки
        :raises ValueError: Если передан объект, не являющийся BookCollection
        """
        if books is None:
            self.books = BookCollection()
            self.indexes = IndexDict()
            return
        if not isinstance(books, BookCollection):
            raise ValueError('Библиотеку можно создать только из коллекции книг.')
        self.books = books
        self.indexes = IndexDict(books)

    def remove_book_by_isbn(self, isbn: str) -> None:
        """
        Удаляет книгу по её ISBN из библиотеки. Ничего не возвращает.
        :param isbn: Строка с ISBN книги
        """
        self.indexes.remove_book_by_isbn(isbn)
        self.books.remove_book_by_isbn(isbn)

    def remove_book(self, book: Book) -> None:
        """
        Удаляет указанную книгу из библиотеки. Ничего не возвращает.
        :param book: Объект класса Book или его подклассов
        :raises ValueError: Если передан объект, не являющийся Book
        """
        if not isinstance(book, Book):
            raise ValueError('Библиотека состоит только из объектов типа Book.')
        self.remove_book_by_isbn(book.isbn)

    def add_book(self, book: Book) -> None:
        """
        Добавляет книгу в библиотеку. Ничего не возвращает.
        :param book: Объект класса Book или его подклассов
        :raises ValueError: Если передан объект, не являющийся Book
        """
        if not isinstance(book, Book):
            raise ValueError('Библиотека состоит только из объектов типа Book.')
        self.indexes.add_book(book)
        self.books.add_book(book)

    def find_by_isbn(self, isbn: str) -> Book:
        """
        Возвращает книгу по её ISBN.
        :param isbn: Строка с ISBN
        :return: Объект Book
        """
        return self.indexes.get_by_isbn(isbn)

    def find_by_author(self, author: str) -> list[Book]:
        """
        Возвращает список книг указанного автора.
        :param author: Строка с именем автора
        :return: Список объектов Book
        """
        return self.indexes.get_by_author(author)

    def find_by_year(self, year: int) -> list[Book]:
        """
        Возвращает список книг, изданных в указанном году.
        :param year: Целое число — год издания
        :return: Список объектов Book
        """
        return self.indexes.get_by_year(year)

    def find_by_genre(self, genre: str) -> list[Book]:
        """
        Возвращает список книг указанного жанра.
        :param genre: Строка с жанром книги
        :return: Список объектов Book
        :raises ValueError: Если жанр указан некорректно
        """
        if type(genre) is not str or genre.strip() == '':
            raise ValueError('В поле "genre" ожидается непустая строка.')
        genre = genre.strip().lower()
        res = []
        for book in self.books:
            if book.genre == genre:
                res.append(book)
        return res

    def __len__(self):
        """
        Возвращает количество книг в библиотеке.
        :return: Целое число - размер библиотеки
        """
        return len(self.books)

    def __iter__(self):
        """
        Возвращает итератор по всем книгам в библиотеке.
        :return: Итератор по объектам Book
        """
        return iter(self.books)

