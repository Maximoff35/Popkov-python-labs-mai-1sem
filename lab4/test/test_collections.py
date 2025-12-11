import pytest
from src.models import Book
from src.collections import BookCollection, IndexDict


def sdelat_book(nomer: int) -> Book:
    return Book(f"Book {nomer}", f"Avtor {nomer}", 2000 + nomer, "roman", f"isbn-{nomer}")


def test_collections_pustaya_i_iz_spiska():
    b1, b2 = sdelat_book(1), sdelat_book(2)
    collections_pust = BookCollection()
    assert len(collections_pust) == 0
    collections = BookCollection([b1, b2])
    assert len(collections) == 2
    assert collections[0] == b1
    assert collections[1] == b2


def test_collections_init_krivo():
    with pytest.raises(ValueError):
        BookCollection("ne spisok")


def test_collections_add_i_contains():
    b1 = sdelat_book(1)
    collections = BookCollection()
    collections.add_book(b1)
    assert len(collections) == 1
    assert b1 in collections
    assert collections.contain_isbn(b1.isbn)


def test_collections_add_ne_book():
    collections = BookCollection()
    with pytest.raises(ValueError):
        collections.add_book("eto ne book")


def test_collections_zamena_po_isbn():
    b1 = sdelat_book(1)
    b2 = Book("Drugoe", "Drugoj", 2005, "roman", b1.isbn)
    collections = BookCollection([b1])
    collections.add_book(b2)
    assert len(collections) == 1
    assert collections[0] == b2


def test_collections_remove_po_isbn_norm():
    b1, b2 = sdelat_book(1), sdelat_book(2)
    collections = BookCollection([b1, b2])
    collections.remove_book_by_isbn(b1.isbn)
    assert len(collections) == 1
    assert b1 not in collections
    assert b2 in collections


def test_collections_remove_po_isbn_net_takogo():
    collections = BookCollection()
    with pytest.raises(KeyError):
        collections.remove_book_by_isbn("net_takogo")


@pytest.mark.parametrize("krivoj_isbn", ["", "   ", 123])
def test_collections_remove_krivoj_isbn(krivoj_isbn):
    collections = BookCollection()
    with pytest.raises(ValueError):
        collections.remove_book_by_isbn(krivoj_isbn)


def test_collections_contain_isbn_false():
    collections = BookCollection()
    assert not collections.contain_isbn("kto_tam")


def test_collections_getitem_i_srez():
    b1, b2, b3 = sdelat_book(1), sdelat_book(2), sdelat_book(3)
    collections = BookCollection([b1, b2, b3])
    assert collections[0] == b1
    pod = collections[1:]
    assert isinstance(pod, BookCollection)
    assert len(pod) == 2
    assert pod[0] == b2
    assert pod[1] == b3


def test_collections_getitem_krivoe():
    collections = BookCollection()
    with pytest.raises(ValueError):
        _ = collections["0"]


def test_collections_contains_ne_book():
    collections = BookCollection()
    with pytest.raises(ValueError):
        _ = "ne book" in collections


def test_index_pustoj_i_iz_collections():
    b1, b2 = sdelat_book(1), sdelat_book(2)
    collections = BookCollection([b1, b2])
    idx_pust = IndexDict()
    assert len(idx_pust) == 0
    idx = IndexDict(collections)
    assert len(idx) == 2
    assert idx.get_by_isbn(b1.isbn) == b1
    assert b1.isbn in idx
    assert b2.isbn in idx


def test_index_add_i_gety():
    b1 = sdelat_book(1)
    b2 = sdelat_book(2)
    idx = IndexDict()
    idx.add_book(b1)
    idx.add_book(b2)
    assert idx.get_by_isbn(b1.isbn) == b1
    assert b1.isbn in idx
    po_avtoru = idx.get_by_author(b1.author)
    assert b1 in po_avtoru
    po_godu = idx.get_by_year(b2.year)
    assert b2 in po_godu


def test_index_add_ne_book():
    idx = IndexDict()
    with pytest.raises(ValueError):
        idx.add_book("ya_ne_book")


def test_index_zamena_po_isbn():
    b1 = sdelat_book(1)
    b2 = Book("Novoe", b1.author, b1.year, "roman", b1.isbn)
    idx = IndexDict(BookCollection([b1]))
    idx.add_book(b2)
    assert len(idx) == 1
    assert idx.get_by_isbn(b1.isbn) == b2


def test_index_remove_book_i_ochistka():
    b1, b2 = sdelat_book(1), sdelat_book(2)
    idx = IndexDict(BookCollection([b1, b2]))
    idx.remove_book(b1)
    assert len(idx) == 1
    vse_isbn = [b.isbn for b in idx]
    assert b1.isbn not in vse_isbn


def test_index_remove_neizvestnuyu_book():
    idx = IndexDict()
    with pytest.raises(KeyError):
        idx.remove_book(sdelat_book(1))


def test_index_remove_ne_book():
    idx = IndexDict()
    with pytest.raises(ValueError):
        idx.remove_book("chto_eto")


def test_index_remove_po_isbn_net_takogo():
    idx = IndexDict()
    with pytest.raises(KeyError):
        idx.remove_book_by_isbn("net_takogo")


@pytest.mark.parametrize("krivoj_isbn", ["", "   ", 123])
def test_index_remove_po_isbn_krivo(krivoj_isbn):
    idx = IndexDict()
    with pytest.raises(ValueError):
        idx.remove_book_by_isbn(krivoj_isbn)


def test_index_get_po_avtoru_net_i_krivo():
    idx = IndexDict()
    with pytest.raises(KeyError):
        idx.get_by_author("Neizvestnyj")
    with pytest.raises(ValueError):
        idx.get_by_author("  ")


def test_index_get_po_godu_net_i_krivo():
    idx = IndexDict()
    with pytest.raises(KeyError):
        idx.get_by_year(2000)
    with pytest.raises(ValueError):
        idx.get_by_year("2000")


def test_index_getitem_setitem_i_contains():
    b1 = sdelat_book(1)
    idx = IndexDict()
    idx[b1.isbn] = b1
    assert idx[b1.isbn] == b1
    assert b1.isbn in idx


def test_index_setitem_ne_tot_isbn():
    b1 = sdelat_book(1)
    idx = IndexDict()
    with pytest.raises(ValueError):
        idx["drugoj"] = b1
