from src.simulation import run_simulation


def main() -> None:
    """
    Точка входа.
    :return: Ничего не возвращает.
    """

    n = input('Введите количество шагов симуляции (целое число >= 10): ')
    try:
        n = int(n)
        run_simulation(n)
    except ValueError:
        print('Введено некорректное число шагов. Симуляция завершает работу.')

if __name__ == '__main__':
    main()