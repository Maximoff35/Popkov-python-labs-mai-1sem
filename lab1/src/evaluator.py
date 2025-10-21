from src import errors


def eval_rpn(rpn: list) -> int | float:
    """
    Вычисляет арифметическое выражение по записи в обратной польской нотации.

    :param rpn: Список токенов в обратной польской нотации.
    :return: Результат арифметического выражения - целое или вещественное число
    """

    stek = []
    for token in rpn:
        if token[0] == 'NUM':
            if token[1] == int(token[1]):
                stek.append(int(token[1]))
            else:
                stek.append(token[1])
        elif token[0] == 'OP':
            if token[1] == 'NEG':
                stek[-1] *= (-1)
            else:
                a = stek.pop()
                if token[1] == '+':
                    stek[-1] += a
                elif token[1] == '-':
                    stek[-1] -= a
                elif token[1] == '*':
                    stek[-1] *= a
                elif token[1] == '**':
                    stek[-1] **= a
                elif token[1] in ('/', '//', '%'):
                    if a == 0:
                        raise errors.EvalError('Ошибка: деление на 0.')
                    if token[1] in ('//', '%') and (a != int(a) or stek[-1] != int(stek[-1])):
                        raise errors.EvalError(f'Операция {token[1]} определена только для целых чисел.')
                    if token[1] == '/':
                        stek[-1] /= a
                        if stek[-1] == int(stek[-1]):
                            stek[-1] = int(stek[-1])
                    elif token[1] == '//':
                        stek[-1] //= a
                    elif token[1] == '%':
                        stek[-1] %= a
                    else:
                        raise errors.EvalError(f'Неизвестный токен {token} при вычислении.')

    if len(stek) != 1:
        raise errors.EvalError(f'После вычислений в стеке осталось не ровно одно число.')

    return stek[0]
