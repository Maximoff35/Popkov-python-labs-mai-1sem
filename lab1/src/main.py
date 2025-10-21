import calculator

def main() -> None:
    """
    Является точкой входа в приложение
    :return: Данная функция ничего не возвращает
    """

    virazhenie = input('Введите выражение: ')

    result = calculator.calc(virazhenie)

    print('Результат: ', result)


if __name__ == "__main__":
    main()