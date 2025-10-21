from src import tokenizer
from src import parser
from src import evaluator


def calc(virazhenie: str) -> float | int:
    """
    Вычисляет значение арифметического выражения.

    :param virazhenie: Строка, являющаяся арифместическим выражением
    :return: Целое или вещественное число - результат вычислений
    """

    tokens = tokenizer.tokenize(virazhenie)
    tokens = parser.annotate_unary(tokens)
    parser.correctness_check(tokens)
    rpn = parser.to_rpn(tokens)
    result = evaluator.eval_rpn(rpn)

    return result
