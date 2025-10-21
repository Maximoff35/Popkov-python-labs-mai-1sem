from src import constants
from src import errors


def annotate_unary(tokens: list) -> list:
    """
    Определяет унарные минусы и игнорирует унарные плюсы.

    :param tokens: Список токенов без выделенных унарных минусов
    :return: Список токенов, в котором унарные минусы отмечены тегом NEG
    """
    new_tokens = []
    last_token = None
    for token in tokens:
        if token[1] == '-' and last_token in constants.UNARY_LEFT:
            new_tokens.append(('OP', 'NEG'))
        elif token[1] == '+' and last_token in constants.UNARY_LEFT:
            continue
        else:
            new_tokens.append(token)
        last_token = token[0]
    return new_tokens


def correctness_check(tokens: list) -> None:
    """
    Проверяет корректность переданного арифметического выражения.

    :param tokens: Список токенов, в котором определены унарные минусы
    :return: Ничего не возвращает, выбрасывает ошибку ParseError, если находит некорректность
    """
    if tokens == []:
        raise errors.ParseError('Нет токенов.')
    last_token = tokens[0]
    if last_token[0] == 'OP' and last_token[1] != 'NEG' or last_token[0] == 'RP':
        raise errors.ParseError(f'Недопустимый токен {last_token[1]} в начале последовательности.')

    if last_token[0] == 'LP':
        cnt_skobki = 1
    else:
        cnt_skobki = 0

    for token in tokens[1:]:
        if token[0] == 'NUM':
            if last_token[0] in ['NUM', 'RP']:
                raise errors.ParseError(f'Ошибка синтаксиса: {last_token[1]} {token[1]}.')
        elif token[0] == 'OP' and token[1] != 'NEG':
            if last_token[0] in ['OP', 'LP']:
                raise errors.ParseError(f'Ошибка синтаксиса: {last_token[1]} {token[1]}.')
        elif token[0] == 'LP':
            cnt_skobki += 1
            if last_token[0] in ['NUM', 'RP']:
                raise errors.ParseError(f'Ошибка синтаксиса: {last_token[1]} {token[1]}.')
        elif token[0] == 'RP':
            cnt_skobki -= 1
            if last_token[0] in ['LP', 'OP']:
                raise errors.ParseError(f'Ошибка синтаксиса: {last_token[1]} {token[1]}.')
        last_token = token

    if tokens[-1][0] in ('LP', 'OP'):
        raise errors.ParseError(f'Недопустимый токен {tokens[-1][1]} в конце последовательности.')

    if cnt_skobki != 0:
        raise errors.ParseError(f'Число открывающихся скобок не равно числу закрывающихся.')


def to_rpn(tokens: list) -> list:
    """
    Меняем порядок токенов, дано обычное выражение, создает обратную польскую нотацию.

    :param tokens: Список токенов в обычном порядке
    :return: Список токенов в соответствии с обратной польской нотацией
    """

    rpn = []
    op_stek = []
    for token in tokens:
        if token[0] == 'NUM':
            rpn.append(token)
        elif token[0] == 'LP':
            op_stek.append(token)
        elif token[0] == 'OP':
            ejection_condition = constants.ASSOCIATIVITY[token[1]]
            while op_stek:
                if op_stek[-1][0] == 'LP':
                    break
                if ejection_condition(constants.PRIORITY[token[1]], constants.PRIORITY[op_stek[-1][1]]):
                    rpn.append(op_stek.pop())
                else:
                    break
            op_stek.append(token)
        elif token[0] == 'RP':
            while op_stek != [] and op_stek[-1][0] != 'LP':
                rpn.append(op_stek.pop())
            if op_stek == []:
                raise errors.ParseError('Ошибка в скобочных выражениях.')
            else:
                op_stek.pop()
        else:
            raise errors.ParseError(f'Неизвестный токен {token}.')

    while op_stek:
        if op_stek[-1][0] == 'LP':
            raise errors.ParseError('Ошибка в скобочных выражениях.')
        rpn.append(op_stek.pop())

    return rpn
