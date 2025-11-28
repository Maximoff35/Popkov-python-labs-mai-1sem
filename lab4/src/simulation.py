from src.models import Book, FictionBook, ScienceBook
from src.library import Library
from src.constants import *
import random
from src import log


def generate_random_book() -> Book:
    """
    Генерирует случайный объект книги.
    :return: Объект класса Book или его подклассов
    """
    rand_title = random.choice(TITLES)
    rand_author = random.choice(AUTHORS)
    rand_genre = random.choice(GENRES)
    rand_year = random.randrange(2026)
    rand_isbn = ''.join([ISBN_ALPH[random.randrange(len(ISBN_ALPH))] for _ in range(13)])
    rand_class = random.choice(['Book', 'FictionBook', 'ScienceBook'])
    if rand_class == 'Book':
        return Book(rand_title, rand_author, rand_year, rand_genre, rand_isbn)
    elif rand_class == 'FictionBook':
        rand_age_limit = random.randrange(22)
        return FictionBook(rand_title, rand_author, rand_year, rand_genre, rand_isbn, rand_age_limit)
    else:
        rand_field = random.choice(FIELDS)
        return ScienceBook(rand_title, rand_author, rand_year, rand_genre, rand_isbn, rand_field)


def run_simulation(steps: int = 50, seed: int | None = None) -> None:
    """
    Запускает имитацию работы библиотеки. Ничего не возвращает.
    :param steps: Общее количество шагов симуляции (натуральное число >= 10)
    :raises ValueError: Если параметр steps указан некорректно
    """

    def _add():
        book = generate_random_book()
        library.add_book(book)
        log.log_ok(f'[Шаг {step}] ADD: {book}')

    def _remove():
        if not library:
            log.log_ok(f'[Шаг {step}] пропущен, так как библиотека пуста')
            return
        book = random.choice(list(library))
        library.remove_book(book)
        log.log_ok(f'[Шаг {step}] REMOVE: {book}')

    def _find_by_isbn() -> None:
        if not library:
            log.log_ok(f'[Шаг {step}] пропущен, так как библиотека пуста')
            return
        book = random.choice(list(library))
        new_book = library.find_by_isbn(book.isbn)
        log.log_ok(f'[Шаг {step}] FIND_BY_ISBN [{book.isbn}]: {new_book}')

    def _find_by_author() -> None:
        if not library:
            log.log_ok(f'[Шаг {step}] пропущен, так как библиотека пуста')
            return
        book = random.choice(list(library))
        book_lst = library.find_by_author(book.author)
        log.log_ok(f'[Шаг {step}] FIND_BY_AUTHOR [{book.author}]: {book_lst}')

    def _find_by_year() -> None:
        if not library:
            log.log_ok(f'[Шаг {step}] пропущен, так как библиотека пуста')
            return
        book = random.choice(list(library))
        book_lst = library.find_by_year(book.year)
        log.log_ok(f'[Шаг {step}] FIND_BY_YEAR [{book.year}]: {book_lst}')

    def _find_by_genre() -> None:
        if not library:
            log.log_ok(f'[Шаг {step}] пропущен, так как библиотека пуста')
            return
        book = random.choice(list(library))
        book_lst = library.find_by_genre(book.genre)
        log.log_ok(f'[Шаг {step}] FIND_BY_GENRE [{book.genre}]: {book_lst}')

    def _find_invalid_isbn() -> None:
        fake_isbn = ''.join([random.choice(['x', 'y', 'z', '-']) for _ in range(13)])
        try:
            book = library.find_by_isbn(fake_isbn)
            log.log_ok(f'[Шаг {step}] FIND_INVALID_ISBN [{fake_isbn}]: {book}')
        except (ValueError, KeyError) as e:
            log.log_error(f'[Шаг {step}] FIND_INVALID_ISBN [{fake_isbn}]')
            log.log_error(f'[Шаг {step}] {e}')

    def _find_invalid_year() -> None:
        fake_year = random.randrange(3000, 4000)
        try:
            book_lst = library.find_by_year(fake_year)
            log.log_ok(f'[Шаг {step}] FIND_INVALID_YEAR [{fake_year}]: {book_lst}')
        except (ValueError, KeyError) as e:
            log.log_error(f'[Шаг {step}] FIND_INVALID_YEAR [{fake_year}]')
            log.log_error(f'[Шаг {step}] {e}')

    if type(steps) is not int or steps <= 9:
        raise ValueError('Параметр "steps" может принимать только натуральные значения >= 10.')
    library = Library()

    if seed is not None and type(seed) is not int:
        raise ValueError('Параметр "seed" может принимать только целочисленные значения.')
    if seed is not None:
        random.seed(seed)

    commands = [
        _add,
        _remove,
        _find_invalid_year,
        _find_invalid_isbn,
        _find_by_year,
        _find_by_isbn,
        _find_by_genre,
        _find_by_author,
    ]

    log.init_logger()
    log.log_ok('==== СТАРТ СИМУЛЯЦИИ ====')

    # for step in range(10):
    #     _add()
    # for step in range(10, steps):
    #     random.choice(commands)()

    for step in range(steps):
        random.choice(commands)()

    log.log_ok(f'ИТОГ: в библиотеке {len(library)} книг(и).')
    log.log_ok('==== КОНЕЦ СИМУЛЯЦИИ ====')
