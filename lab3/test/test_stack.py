import pytest
from src.stack import Stack


def test_init_empty():
    stek = Stack()
    assert stek.is_empty()
    assert len(stek) == 0


def test_init_with_list_of_ints():
    stek = Stack([1, 2, 3])
    assert not stek.is_empty()
    assert len(stek) == 3
    assert stek.peek() == 3
    assert stek.min() == 1


def test_init_with_list_mixed_types():
    stek = Stack([1, 2, 'a'])
    assert len(stek) == 3
    assert stek.peek() == 'a'
    with pytest.raises(ValueError):
        stek.min()
    stek.pop()
    assert stek.min() == 1


def test_init_wrong_type():
    with pytest.raises(ValueError):
        Stack(123)
    with pytest.raises(ValueError):
        Stack('abc')
    with pytest.raises(ValueError):
        Stack((1, 2, 3))


def test_push_pop_and_len():
    stek = Stack()
    stek.push('a')
    stek.push('b')
    stek.push('c')
    assert len(stek) == 3
    assert stek.pop() == 'c'
    assert len(stek) == 2
    assert stek.pop() == 'b'
    assert stek.pop() == 'a'
    assert stek.is_empty()


def test_peek_does_not_remove():
    stek = Stack()
    stek.push(10)
    stek.push(20)
    assert stek.peek() == 20
    assert len(stek) == 2
    assert stek.peek() == 20
    assert len(stek) == 2


def test_lifo_property():
    stek = Stack()
    znacheniya = [1, 2, 3, 4, 5]
    for x in znacheniya:
        stek.push(x)
    res = [stek.pop() for _ in range(len(znacheniya))]
    assert res == list(reversed(znacheniya))


def test_min_only_numbers():
    stek = Stack()
    stek.push(5)
    assert stek.min() == 5
    stek.push(3)
    assert stek.min() == 3
    stek.push(10.5)
    assert stek.min() == 3
    stek.pop()
    assert stek.min() == 3
    stek.pop()
    assert stek.min() == 5


def test_min_with_mixed_types():
    stek = Stack()
    stek.push(5)
    stek.push(2)
    assert stek.min() == 2
    stek.push('abc')
    with pytest.raises(ValueError):
        stek.min()
    stek.pop()
    assert stek.min() == 2
    stek.push([1, 2, 3])
    with pytest.raises(ValueError):
        stek.min()


def test_min_on_stack_created_from_list():
    stek = Stack([10, 5, 7])
    assert stek.min() == 5
    stek.pop()
    assert stek.min() == 5
    stek.pop()
    assert stek.min() == 10


def test_pop_empty_raises():
    stek = Stack()
    with pytest.raises(IndexError):
        stek.pop()


def test_peek_empty_raises():
    stek = Stack()
    with pytest.raises(IndexError):
        stek.peek()


def test_min_empty_raises():
    stek = Stack()
    with pytest.raises(IndexError):
        stek.min()
