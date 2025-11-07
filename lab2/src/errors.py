class HistoryReadError(Exception):
    '''
    Ошибка при чтении истории.
    '''
    pass


class LsError(Exception):
    '''
    Ошибка при выполнении ls
    '''
    pass


class CdError(Exception):
    '''
    Ошибка при выполнении cd
    '''
    pass


class CatError(Exception):
    '''
    Ошибка при выполнении cat
    '''
    pass


class RmError(Exception):
    '''
    Ошибка при выполнении rm
    '''
    pass


class CpError(Exception):
    '''
    Ошибка при выполнении cp
    '''
    pass


class MvError(Exception):
    '''
    Ошибка при выполнении mv
    '''
    pass


class HistoryError(Exception):
    '''
    Ошибка при выполнении команды history
    '''
    pass


class UndoError(Exception):
    '''
    Ошибка при выполнении команды undo
    '''
    pass


class ZipError(Exception):
    '''
    Ошибка при выполнении команды zip
    '''
    pass


class UnzipError(Exception):
    '''
    Ошибка при выполнении команды unzip
    '''
    pass


class TarError(Exception):
    '''
    Ошибка при выполнении команды tar
    '''
    pass


class UntarError(Exception):
    '''
    Ошибка при выполнении команды untar
    '''
    pass