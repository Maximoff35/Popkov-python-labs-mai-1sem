import pytest
from src.models import Book
from src.collections import BookCollection
from src.library import Library


def sdelat_book(nomer: int) -> Book:
    return Book(f"Book {nomer}", f"Avtor {nomer}", 2000 + nomer, "roman", f"isbn-{nomer}")


def test_library_init_pustoj_i_s_collections():
    lib_pust = Library()
    assert len(lib_pust) == 0
    b1, b2 = sdelat_book(1), sdelat_book(2)
    collections = BookCollection([b1, b2])
    lib = Library(collections)
    assert len(lib) == 2
    vse_books = list(lib)
    assert vse_books[0] == b1
    assert vse_books[1] == b2


def test_library_init_krivo():
    with pytest.raises(ValueError):
        Library("ne_to")


def test_library_add_i_remove_book():
    lib = Library()
    b1, b2 = sdelat_book(1), sdelat_book(2)
    lib.add_book(b1)
    lib.add_book(b2)
    assert len(lib) == 2
    lib.remove_book(b1)
    assert len(lib) == 1
    assert b1 not in list(lib)
    lib.remove_book_by_isbn(b2.isbn)
    assert len(lib) == 0


def test_library_add_ne_book():
    lib = Library()
    with pytest.raises(ValueError):
        lib.add_book("ya_ne_book")


def test_library_remove_ne_book():
    lib = Library()
    with pytest.raises(ValueError):
        lib.remove_book("chto_eto")


def test_library_poisk_po_vsem_polyam():
    lib = Library()
    b1 = Book("Clean Code", "Robert Martin", 2008, "uchebnik", "isbn-1")
    b2 = Book("Drugaya", "Robert Martin", 2010, "uchebnik", "isbn-2")
    b3 = Book("Prosto kniga", "Kto-to", 2010, "roman", "isbn-3")
    lib.add_book(b1)
    lib.add_book(b2)
    lib.add_book(b3)
    naiden_po_isbn = lib.find_by_isbn("isbn-1")
    assert naiden_po_isbn == b1
    po_avtoru = lib.find_by_author("Robert Martin")
    assert b1 in po_avtoru
    assert b2 in po_avtoru
    po_godu = lib.find_by_year(2010)
    assert b2 in po_godu
    assert b3 in po_godu
    po_zhanru = lib.find_by_genre("uchebnik")
    assert b1 in po_zhanru
    assert b2 in po_zhanru
    assert b3 not in po_zhanru


def test_library_find_by_genre_krivo():
    lib = Library()
    with pytest.raises(ValueError):
        lib.find_by_genre("  ")
