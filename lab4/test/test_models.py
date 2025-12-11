import pytest
from src.models import Book, FictionBook, ScienceBook


def test_book_norm_rabotaet():
    book = Book("  Book  ", "  Avtor  ", 2020, " Roman ", " 123-456 ")
    assert book.title == "Book"
    assert book.author == "Avtor"
    assert book.year == 2020
    assert book.genre == "roman"
    assert book.isbn == "123-456"


@pytest.mark.parametrize("krivoe_zagolovok", ["", "   ", 123])
def test_book_plohoe_nazvanie(krivoe_zagolovok):
    with pytest.raises(ValueError):
        Book(krivoe_zagolovok, "Avtor", 2020, "roman", "isbn")


@pytest.mark.parametrize("krivoj_avtor", ["", "   ", 123])
def test_book_plohoj_avtor(krivoj_avtor):
    with pytest.raises(ValueError):
        Book("Book", krivoj_avtor, 2020, "roman", "isbn")


@pytest.mark.parametrize("krivoj_god", ["2020", 2.5])
def test_book_ne_celoe_god(krivoj_god):
    with pytest.raises(ValueError):
        Book("Book", "Avtor", krivoj_god, "roman", "isbn")


@pytest.mark.parametrize("krivoj_god", [-1, 3000])
def test_book_god_vne_diapazona(krivoj_god):
    with pytest.raises(ValueError):
        Book("Book", "Avtor", krivoj_god, "roman", "isbn")


@pytest.mark.parametrize("krivoj_zhanr", ["", "   ", 123])
def test_book_plohoj_zhanr(krivoj_zhanr):
    with pytest.raises(ValueError):
        Book("Book", "Avtor", 2020, krivoj_zhanr, "isbn")


@pytest.mark.parametrize("krivoj_isbn", ["", "   ", 123])
def test_book_plohoj_isbn(krivoj_isbn):
    with pytest.raises(ValueError):
        Book("Book", "Avtor", 2020, "roman", krivoj_isbn)


def test_book_repr_vse_pole():
    book = Book("Book", "Avtor", 2020, "roman", "ISBN123")
    tekst = repr(book)
    assert "Book" in tekst
    assert "Avtor" in tekst
    assert "2020" in tekst
    assert "roman" in tekst
    assert "ISBN123" in tekst


def test_book_sravnenie_po_vsemu():
    k1 = Book("T", "A", 2000, "g", "isbn")
    k2 = Book("T", "A", 2000, "g", "isbn")
    k3 = Book("T2", "A", 2000, "g", "isbn")
    assert k1 == k2
    assert k1 != k3


def test_book_sravnenie_s_bredom():
    k = Book("T", "A", 2000, "g", "isbn")
    assert k.__eq__(42) is NotImplemented


def test_hudozhka_bez_vozrasta_zero():
    hud = FictionBook("T", "A", 2000, "g", "isbn")
    assert hud.age_limit == 0


def test_hudozhka_s_limitom_ok():
    hud = FictionBook("T", "A", 2000, "g", "isbn", 16)
    assert hud.age_limit == 16
    tekst = repr(hud)
    assert "[FICTION]" in tekst
    assert "16+" in tekst


@pytest.mark.parametrize("krivoj_limit", [-1, "18"])
def test_hudozhka_krivoj_limit(krivoj_limit):
    with pytest.raises(ValueError):
        FictionBook("T", "A", 2000, "g", "isbn", krivoj_limit)


def test_nauchnaya_norm_field_i_repr():
    nauka = ScienceBook("T", "A", 2000, "g", "isbn", " Fizika ")
    assert nauka.field == "fizika"
    tekst = repr(nauka)
    assert "[SCIENCE]" in tekst
    assert "fizika" in tekst


@pytest.mark.parametrize("krivoe_pole", ["", "   ", 123])
def test_nauchnaya_krivoe_pole(krivoe_pole):
    with pytest.raises(ValueError):
        ScienceBook("T", "A", 2000, "g", "isbn", krivoe_pole)
