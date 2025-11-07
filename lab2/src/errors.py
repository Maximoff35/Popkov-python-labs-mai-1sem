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