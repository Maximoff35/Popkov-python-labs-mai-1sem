from src import calculator


def main() -> None:
    """
    Является точкой входа в приложение
    :return: Данная функция ничего не возвращает
    """

    virazhenie = input('Введите выражение: ')

    try:
        result = calculator.calc(virazhenie)
        print('Результат:', result)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
