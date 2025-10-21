from src.constants import TOKEN_RE
from src.errors import TokenizeError


def tokenize(virazhenie: str) -> list:
    """
    Берет арифметическое выражение и разбивает его на токены - числа, операции, скобки.

    :param virazhenie: Строка, являющаяся арифместическим выражением
    :return: Список токенов
    """

    tokens = []
    for i in TOKEN_RE.finditer(virazhenie):
        if i.lastgroup == 'MIS':
            raise TokenizeError(f'Ошибочный токен: {i.group()}')
        elif i.lastgroup != 'WS':
            if i.lastgroup == 'NUM':
                if '.' in i.group():
                    tokens.append((i.lastgroup, float(i.group())))
                else:
                    tokens.append((i.lastgroup, int(i.group())))
            else:
                tokens.append((i.lastgroup, i.group()))

    return tokens
