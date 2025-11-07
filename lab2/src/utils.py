from pathlib import Path
import datetime
from src import constants as ct


def _permissions_str(mode: int) -> str:
    '''
    Переделывает st_mode в короткую строку с правами
    :param mode: st_mode
    :return: короткая запись, например, rwxr-xr--
    '''
    flags = [
        (0o400, 'r'), (0o200, 'w'), (0o100, 'x'),
        (0o040, 'r'), (0o020, 'w'), (0o010, 'x'),
        (0o004, 'r'), (0o002, 'w'), (0o001, 'x'),
    ]
    result = []
    for bit, ch in flags:
        if mode & bit:
            result.append(ch)
        else:
            result.append('-')
    return ''.join(result)


def _uniq_path_trash(cp: Path) -> Path:
    '''
    Делаем уникальный путь внутри корзины с пометкой времени
    :param cp: текущий путь
    :return: Уникальный путь внутри корзины
    '''
    tm = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    name = f'{cp.stem}_{tm}{cp.suffix}'
    cand = ct.TRASH_DIR / name
    i = 1
    while cand.exists():
        name = f'{cp.stem}_{tm}_{i}{cp.suffix}'
        cand = ct.TRASH_DIR / name
        i += 1
    return cand
