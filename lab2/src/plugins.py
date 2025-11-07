from src.errors import HistoryError, UndoError, ZipError, UntarError, UnzipError, TarError
from src import store
from src.store import undo_pop
from pathlib import Path
from src.fs import get_path
import shutil
import zipfile
import tarfile

def command_history(state, args: list[str], opts: set[str]) -> list[str]:
    '''
    Возвращает список последних N введенных команд с их номерами
    :param state: Объект состояния, в котором есть текущий каталог
    :param args: Аргументы (например путь)
    :param opts: Опции типа -l итд
    :return: Список строк для вывода пользователю
    '''

    n = None
    if args:
        try:
            n = int(args[0])
        except:
            raise HistoryError('N должно быть положительным и целым числом')
        if n <= 0:
            raise HistoryError('N должно быть положительным и целым числом')
    elif opts:
        try:
            n = int(opts[0])
        except:
            raise HistoryError('N должно быть положительным и целым числом')
        if n <= 0:
            raise HistoryError('N должно быть положительным и целым числом')
    lines = store.history_read(n)
    if lines == []:
        return ['пусто']
    else:
        res = []
        for i in range(len(lines)):
            res.append(f'{i + 1} {lines[i]}')
        return res


def command_undo(state, args: list[str], opts: set[str]) -> list[str]:
    '''
    Отменяет последнюю команду из списка cp, mv, rm.
    :param state: Объект состояния
    :param args: Аргументы
    :param opts: Опции
    :return: Список строк для вывода пользователю
    '''

    inf = undo_pop()
    if not inf:
        return ['Нет доступных к отмене команд cp, mv, rm.']
    op = inf.get('op')
    old_path = Path(inf.get('old_path', ''))
    new_path = Path(inf.get('new_path', ''))
    is_dir = inf.get('is_dir', False)

    try:
        if op == 'rm':
            if not new_path.exists():
                raise UndoError('Файл/каталог не найден в корзине.')
            if old_path.exists():
                raise UndoError('На месте восстановления уже есть объект с таким же названием.')
            shutil.move(new_path, old_path)
            return [f'Отмена rm: объект {old_path.name} восстановлен из корзины.']

        elif op == 'cp':
            if not new_path.exists():
                raise UndoError('Объект уже удален.')
            if is_dir:
                shutil.rmtree(new_path)
            else:
                new_path.unlink()
            return [f'Отменя cp: объект {new_path.name} удален.']

        elif op == 'mv':
            if not new_path.exists():
                raise UndoError('Объект, который хотите вернуть, не найден.')
            if old_path.exists():
                raise UndoError('На месте восстановления уже есть объект с таким же названием.')
            shutil.move(new_path, old_path)
            return [f'Отмена mv: объект {old_path.name} восстановлен на прежнем месте.']

        else:
            return [f'Операция {op} не поддерживается в undo.']

    except PermissionError:
        raise UndoError(f'Нет прав при отмене {op}.')
    except UndoError as e:
        raise UndoError(str(e))
    except Exception as e:
        raise UndoError(f'Ошибка при отмене {op}: {e}.')


def command_zip(state, args: list[str], opts: set[str]) -> list[str]:
    '''
    Создание архива формата ZIP из каталога
    Пример: zip <папка> <архив.zip>
    :param state: Объект состояния
    :param args: Аргументы
    :param opts: Опции
    :return: Список строк для вывода пользователю
    '''

    if len(args) < 2:
        raise ZipError('Необходимо указать исходный каталог и путь к архиву .zip.')

    old, new = [i.strip() for i in args[:2]]

    try:
        old_path = get_path(old, state.cwd)
        new_path = get_path(new, state.cwd)
    except:
        raise ZipError('Некорректный путь.')

    if not old_path.exists():
        raise ZipError('Каталог не найден по указанному пути.')
    if not old_path.is_dir():
        raise ZipError('По указанному пути находится не каталог.')
    if new_path.exists():
        raise ZipError('Объект с таким названием уже существует.')
    if new_path.suffix.lower() != '.zip':
        raise ZipError('У архива должно быть расширение .zip.')
    if not new_path.parent.exists():
        raise ZipError('Каталог, в который необходимо сохранить архив, не найден.')

    try:
        with zipfile.ZipFile(new_path, mode='w', compression=zipfile.ZIP_DEFLATED) as zipka:
            for i in old_path.rglob('*'):
                zipname = i.relative_to(old_path.parent)
                zipka.write(i, zipname)
    except PermissionError:
        raise ZipError('Нет необходимых для архивации прав.')
    except Exception as e:
        raise ZipError(f'Ошибка архивации: {e}.')

    return [f'ZIP-архив {new_path.name} создан из {old_path.name}.']


def command_unzip(state, args: list[str], opts: set[str]) -> list[str]:
    '''
    Распаковка архива ZIP в текущий каталог
    Пример: unzip <архив.zip>
    :param state: Объект состояния
    :param args: Аргументы
    :param opts: Опции
    :return: Список строк для вывода пользователю
    '''

    if len(args) < 1:
        raise UnzipError('Необходимо указать путь к архиву .zip.')
    raw = args[0].strip()

    try:
        zipka_path = get_path(raw, state.cwd)
    except:
        raise UnzipError('Некорректный путь.')

    if not zipka_path.exists():
        raise UnzipError('Архив не обнаружен.')
    if not zipka_path.is_file():
        raise UnzipError('Указанный путь не является файлом.')
    if zipka_path.suffix != '.zip':
        raise UnzipError('Необходимо указать путь к архиву с расширением .zip.')

    try:
        with zipfile.ZipFile(zipka_path, mode='r') as zipka:
            zipka.extractall(state.cwd)
    except PermissionError:
        raise UnzipError('Нет необходимых для распаковки архива прав.')
    except Exception as e:
        raise UnzipError(f'Ошибка распаковки архива: {e}.')

    return [f'Архив {zipka_path.name} успешно распакован в директорию {state.cwd.name}.']


def command_tar(state, args: list[str], opts: set[str]) -> list[str]:
    '''
    Создание архива формата TAR.GZ из каталога
    Пример: tar <папка> <архив.tar.gz>
    :param state: Объект состояния
    :param args: Аргументы
    :param opts: Опции
    :return: Список строк для вывода пользователю
    '''

    if len(args) < 2:
        raise TarError('Необходимо указать исходный каталог и путь к архиву .tar.gz.')

    old, new = [i.strip() for i in args[:2]]

    try:
        old_path = get_path(old, state.cwd)
        new_path = get_path(new, state.cwd)
    except:
        raise TarError('Некорректный путь.')

    if not old_path.exists():
        raise TarError('Каталог не найден по указанному пути.')
    if not old_path.is_dir():
        raise TarError('По указанному пути находится не каталог.')
    if new_path.exists():
        raise TarError('Объект с таким названием уже существует.')
    if new_path.name[-7:] != '.tar.gz':
        raise TarError('У архива должно быть расширение .tar.gz.')
    if not new_path.parent.exists():
        raise TarError('Каталог, в который необходимо сохранить архив, не найден.')

    try:
        with tarfile.open(new_path, mode='w:gz') as tarik:
            tarik.add(old_path, arcname=old_path.name)
    except PermissionError:
        raise TarError('Нет необходимых для архивации прав.')
    except Exception as e:
        raise TarError(f'Ошибка архивации: {e}.')

    return [f'TAR.GZ-архив {new_path.name} создан из {old_path.name}.']


def command_untar(state, args: list[str], opts: set[str]) -> list[str]:
    '''
    Распаковка архива TAR.GZ в текущий каталог
    Пример: untar <архив.tar.gz>
    :param state: Объект состояния
    :param args: Аргументы
    :param opts: Опции
    :return: Список строк для вывода пользователю
    '''

    if len(args) < 1:
        raise UntarError('Необходимо указать путь к архиву .tar.gz.')
    raw = args[0].strip()

    try:
        tarik_path = get_path(raw, state.cwd)
    except:
        raise UntarError('Некорректный путь.')

    if not tarik_path.exists():
        raise UntarError('Архив не обнаружен.')
    if not tarik_path.is_file():
        raise UntarError('Указанный путь не является файлом.')
    if tarik_path.name[-7:] != '.tar.gz':
        raise UntarError('Необходимо указать путь к архиву с расширением .tar.gz.')

    try:
        with tarfile.open(tarik_path, mode='r:gz') as tarik:
            tarik.extractall(state.cwd)
    except PermissionError:
        raise UntarError('Нет необходимых для распаковки архива прав.')
    except Exception as e:
        raise UntarError(f'Ошибка распаковки архива: {e}.')

    return [f'Архив {tarik_path.name} успешно распакован в директорию {state.cwd.name}.']