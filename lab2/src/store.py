from datetime import datetime
import logging
from src.errors import HistoryReadError
from src import constants as ct
import json


def init_storage() -> None:
    '''
    Создает storage/, .trash/ и служебные файлы при первом запуске.
    :return: Ничего не возвращает
    '''

    ct.STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    ct.TRASH_DIR.mkdir(parents=True, exist_ok=True)

    if not ct.LOG_FILE.exists():
        ct.LOG_FILE.touch()
    if not ct.HISTORY_FILE.exists():
        ct.HISTORY_FILE.touch()
    if not ct.UNDO_FILE.exists():
        ct.UNDO_FILE.write_text('[]', encoding='utf-8')

    logging.basicConfig(
        filename=ct.LOG_FILE,
        level=logging.INFO,
        format="[%(asctime)s] %(message)s",
        datefmt=ct.LOG_TIME_FORMAT,
        encoding='utf-8',
    )


def time_now() -> str:
    '''
    Возвращает текущее время в соответствии с форматом из constants.py
    :return: Возвращает текущее время
    '''
    return datetime.now().strftime(ct.LOG_TIME_FORMAT)


def log_ok(message: str) -> None:
    '''
    Записывает в лог обычное сообщение.
    :param message: Что записываем в лог.
    :return: Ничего не возвращает.
    '''
    logging.info(message)


def log_error(message: str) -> None:
    '''
        Записывает в лог ошибку.
        :param message: Что записываем в лог.
        :return: Ничего не возвращает.
        '''
    logging.error(message)


def history_append(command: str) -> None:
    '''
    Добавляет команду в файл с историей.
    :param command: Команда.
    :return: Ничего не возвращает.
    '''

    with open(ct.HISTORY_FILE, 'a', encoding='utf-8') as his_file:
        his_file.write(command + '\n')


def history_read(n: int | None = None) -> list[str]:
    '''
    Читает из истории или все команды, или последние n.
    :param n: Количество читаемых команд, None - если нужны все.
    :return: Возвращает список строк - команды.
    '''

    with open(ct.HISTORY_FILE, encoding='utf-8') as his_file:
        lines = [line.strip() for line in his_file]

    if n is None:
        return lines
    else:
        if n < 0 or n > len(lines):
            raise HistoryReadError('Недопустимое количество команд.')
        return lines[-n:]


def append_undo_rec(rec: dict) -> None:
    '''
    Дописываем запись в JSON UNDO_FILE
    :param rec: dict с информацией про операцию
    :return: Ничего не возвращает
    '''
    try:
        if ct.UNDO_FILE.exists():
            raw_text = ct.UNDO_FILE.read_text(encoding='utf-8').strip()
            if raw_text:
                data = json.loads(raw_text)
            else:
                data = []
        else:
            data = []
    except Exception:
        data = []
    data.append(rec)
    ct.UNDO_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def undo_pop() -> dict | None:
    '''
    Достаем последнюю операцию из .undo.json и удаляем ее оттуда
    :return: dict с информацией про последнюю операцию или None
    '''
    try:
        if ct.UNDO_FILE.exists():
            raw_text = ct.UNDO_FILE.read_text(encoding='utf-8').strip()
            if raw_text:
                data = json.loads(raw_text)
            else:
                data = []
        else:
            data = []
    except Exception:
        data = []
    if not data:
        return None
    last = data.pop()

    ct.UNDO_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

    return last



