import logging
from src.constants import LOG_FILE, LOG_TIME_FORMAT, LOG_FORMAT


def init_logger() -> None:
    """
    Создает shell.log при первом запуске
    :return: Ничего не возвращает
    """
    if not LOG_FILE.exists():
        LOG_FILE.touch()
    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
        datefmt=LOG_TIME_FORMAT,
        handlers=[
            logging.FileHandler(LOG_FILE, encoding='utf-8'),
            logging.StreamHandler(),
        ],
    )


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