# Лабораторная работа №3. Алгоритмический мини-пакет
Попков Максим Александрович  
Группа: М8О-105БВ-25

## Цель и результаты
- Реализовать набор алгоритмов вычисления факториала и чисел Фибоначчи.  
- Освоить базовые алгоритмы сортировки (пузырьковая, быстрая, подсчётом, поразрядная, карманная, пирамидальная).  
- Разработать структуру данных **Стек** с поддержкой операции `min()` за O(1).  
- Написать модульные тесты с использованием PyTest.

## Структура проекта

```
.
├── lab3
│   ├── src/
│   │   ├── factorial_and_fibo.py
│   │   ├── sorts.py
│   │   └── stack.py
│   ├── test/
│   │   ├── test_factorial_and_fibo.py
│   │   ├── test_sorts.py
│   │   └── test_stack.py
│   ├── requirements.txt
│   ├── report.pdf
│   ├── .pre-commit-config.yaml
│   └── README.md
```

## Описание реализованных модулей

### `factorial_and_fibo.py`
Реализованы функции:
- `factorial(n: int) -> int`
- `factorial_recursive(n: int) -> int`
- `fibo(n: int) -> int`
- `fibo_recursive(n: int) -> int`

### `sorts.py`
Реализованы алгоритмы:
- пузырьковая сортировка  
- быстрая сортировка  
- сортировка подсчётом  
- поразрядная сортировка  
- карманная сортировка  
- пирамидальная сортировка  

### `stack.py`
Класс `Stack` с операциями:
- `push`
- `pop`
- `peek`
- `is_empty`
- `__len__`
- `min()` — за O(1)

## Установка и запуск

```
git clone https://github.com/Maximoff35/Popkov-python-labs-mai-1sem
cd <папка_проекта>/lab3
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Тестирование

```
pytest -v
```

Тесты включают:
- factorial/fibo,
- сортировки,
- стек и min(),
- проверки ошибок.
