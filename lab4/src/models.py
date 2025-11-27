class Book:
    """
    Модель книги в библиотеке.

    Хранит основные сведения о книге: название, автора,
    год издания, жанр и уникальный ISBN. Используется
    в пользовательских коллекциях и индексах.
    """

    def __init__(self, title: str, author: str, year: int, genre: str, isbn: str) -> None:
        """
        Инициализация класса. Ничего не возвращает.
        :param title: Название
        :param author: Автор
        :param year: Год
        :param genre: Жанр
        :param isbn: Код ISBN
        """
        if type(title) is not str or title.strip() == '':
            raise ValueError('В поле "title" ожидается непустая строка.')
        if type(author) is not str or author.strip() == '':
            raise ValueError('В поле "author" ожидается непустая строка.')
        if type(year) is not int:
            raise ValueError('В поле "year" ожидается целое число.')
        if not (0 <= year <= 2026):
            raise ValueError('Год должен быть от 0 до 2026.')
        if type(genre) is not str or genre.strip() == '':
            raise ValueError('В поле "genre" ожидается непустая строка.')
        if type(isbn) is not str or isbn.strip() == '':
            raise ValueError('В поле "isbn" ожидается непустая строка.')

        self.title = title.strip()
        self.author = author.strip()
        self.year = year
        self.genre = genre.strip().lower()
        self.isbn = isbn.strip()

    def __repr__(self) -> str:
        """
        Представление книги в виде строки.
        :return: Возвращает строку из полей title, author, year, genre, isbn
        """
        return f'[{self.year}] {self.author} - "{self.title}" (жанр: {self.genre}, ISBN: {self.isbn})'

    def __eq__(self, other: "Book") -> bool:
        """
        Сравнение двух книг по всем полям.
        :param other: Объект, с которым выполняется сравнение.
        :return: True, если книги совпадают, иначе False.
        """
        if not isinstance(other, Book):
            return NotImplemented
        return (self.isbn == other.isbn and self.year == other.year and self.author == other.author and
                self.title == other.title and self.genre == other.genre)


class FictionBook(Book):
    """
    Класс художественной книги.

    Наследует Book, добавляет поле возрастного ограничения
    и уточнённое строковое представление для логирования.
    """

    def __init__(self, title: str, author: str, year: int, genre: str, isbn: str, age_limit: int | None = None) -> None:
        """
        Инициализация класса. Ничего не возвращает.
        :param title: Название
        :param author: Автор
        :param year: Год
        :param genre: Жанр
        :param isbn: Код ISBN
        :param age_limit: Возрастное ограничение
        """

        super().__init__(title, author, year, genre, isbn)
        if age_limit is None:
            self.age_limit = 0
        else:
            if type(age_limit) is not int or age_limit < 0:
                raise ValueError('Возрастное ограничение должно быть целым неотрицательным числом.')
            self.age_limit = age_limit

    def __repr__(self):
        """
        Представление художественной книги в виде строки.
        :return: Возвращает строку из полей title, author, year, genre, isbn, age_limit
        """
        base = super().__repr__()
        return f'[FICTION] {base} (возрастное ограничение: {self.age_limit}+)'


class ScienceBook(Book):
    """
    Класс научной книги.

    Наследует Book, добавляет поле области науки
    и расширенное строковое представление для логирования.
    """

    def __init__(self, title: str, author: str, year: int, genre: str, isbn: str, field: str) -> None:
        """
        Инициализация класса. Ничего не возвращает.
        :param title: Название
        :param author: Автор
        :param year: Год
        :param genre: Жанр
        :param isbn: Код ISBN
        :param field: Область науки
        """
        super().__init__(title, author, year, genre, isbn)
        if type(field) is not str or field.strip() == '':
            raise ValueError('В поле "field" ожидается непустая строка.')
        self.field = field.strip().lower()

    def __repr__(self):
        """
        Представление научной книги в виде строки.
        :return: Возвращает строку из полей title, author, year, genre, isbn, field
        """
        base = super().__repr__()
        return f'[SCIENCE] {base} (область науки: {self.field})'
