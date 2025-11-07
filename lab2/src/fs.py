import datetime
from pathlib import Path
from src.errors import *
from src import constants as ct
from src.utils import _permissions_str, _uniq_path_trash
from src.store import append_undo_rec
import shutil


def get_path(raw: str | None, cwd: Path) -> Path:
    '''
    Превращает то, что написал пользователь в настоящий путь на диске.
    :param raw: То, что написал пользователь
    :param cwd: Текущий путь
    :return: Новый путь
    '''

    if not raw:
        return cwd

    raw = raw.strip()
    if not raw or raw == '.':
        return cwd
    if raw[0] == '~':
        if raw == '~':
            return Path.home()
        else:
            return (Path.home() / raw[2:]).resolve(strict=False)
    if Path(raw).is_absolute():
        return Path(raw).resolve(strict=False)
    return (cwd / raw).resolve(strict=False)


def command_ls(state, args: list[str], opts: set[str]) -> list[str]:
    '''
    Возвращает содержимое папки
    :param state: Объект состояния, в котором есть текущий каталог
    :param args: Аргументы (например путь)
    :param opts: Опции типа -l итд
    :return: Список строк для вывода пользователю
    '''
    raw = args[0] if args else None

    try:
        cur_path = get_path(raw, state.cwd)
    except Exception:
        raise LsError('Некорректный путь.')

    if not cur_path.exists():
        raise LsError('Нет такого пути.')
    if not cur_path.is_dir():
        raise LsError('Это не каталог.')

    try:
        ent = sorted(cur_path.iterdir(), key=lambda p: p.name.lower())
    except PermissionError:
        raise LsError('Нет доступа к каталогу.')

    detailed = ('-l' in opts)
    res = []

    if not detailed:
        for p in ent:
            if p.is_dir():
                cur = p.name + '/'
            else:
                cur = p.name
            res.append(cur)
    else:
        for p in ent:
            if p.is_dir():
                name = p.name + '/'
            else:
                name = p.name
            try:
                st = p.stat()
                size = st.st_size
                mtime_ts = st.st_mtime
                mtime = datetime.datetime.fromtimestamp(mtime_ts).strftime(ct.LOG_TIME_FORMAT)
                permissions = _permissions_str(st.st_mode)
                res.append(f'{name} | {size} | {mtime} | {permissions}')
            except PermissionError:
                res.append(f'{name} | ? | ? | ?')
    return res


def command_cd(state, args: list[str], opts: set[str]) -> list:
    '''
    Меняет текущий каталог
    :param state: Объект состояния, в котором есть текущий каталог
    :param args: Аргументы (например путь)
    :param opts: Опции типа -l итд
    :return: Возвращает пустой список
    '''

    if not args:
        state.cwd = Path.home()
        return []

    raw = args[0]
    try:
        cur_path = get_path(raw, state.cwd)
    except Exception:
        raise CdError('Некорректный путь.')
    if not cur_path.exists():
        raise CdError('Нет такого пути.')
    if not cur_path.is_dir():
        raise CdError('Это не каталог.')

    state.cwd = cur_path

    return []


def command_cat(state, args: list[str], opts: set[str]) -> list[str]:
    '''
    Возвращает содержимого указанного файла для вывода в консоль
    :param state: Объект состояния, в котором есть текущий путь
    :param args: Аргументы (например путь)
    :param opts: Опции типа -l итд
    :return: Список строк для вывода пользователю
    '''

    if not args:
        raise CatError('Не указан файл.')

    raw = args[0]
    try:
        cur_path = get_path(raw, state.cwd)
    except Exception:
        raise CatError('Некорректный путь.')
    if not cur_path.exists():
        raise CatError('Нет такого пути.')
    if cur_path.is_dir():
        raise CdError('Это не файл.')

    try:
        with open(cur_path, 'r', encoding='utf-8') as file:
            res = [line.rstrip() for line in file]
    except PermissionError:
        raise CatError('Нет прав на чтение файла.')

    return res


def command_rm(state, args: list[str], opts: set[str]) -> list[str]:
    '''
    Удаляет указанный файл, при -r рекурсивно. Есть поддержка восстановления из корзины
    :param state: Объект состояния, в котором есть текущий путь
    :param args: Аргументы (например путь)
    :param opts: Опции типа -r итд
    :return: Список со строкой об удалении
    '''

    if not args:
        raise RmError('Не указан путь.')

    raw = args[0].strip()

    if raw in ['/', '..']:
        raise RmError('Нельзя удалить корневой или родительский каталог.')

    try:
        cur_path = get_path(raw, state.cwd)
    except Exception:
        raise RmError('Некорректный путь.')

    if not cur_path.exists():
        raise RmError('Нет такого файла/каталога.')

    if cur_path.resolve() == ct.BASE_DIR.resolve():
        raise RmError('Нельзя удалить корневой каталог проекта.')

    if cur_path.is_file():
        tr_path = _uniq_path_trash(cur_path)
        try:
            shutil.move(cur_path, tr_path)
        except PermissionError:
            raise RmError('Нет прав на удаление файла.')
        except OSError as e:
            raise RmError(f'Ошибка удаления файла {e}.')

        append_undo_rec({
            'op': 'rm',
            'old_path': str(cur_path),
            'new_path': str(tr_path),
            'is_dir': False,
            'time': datetime.datetime.now().strftime(ct.LOG_TIME_FORMAT),
        })
        return [f'Файл {cur_path.name} перемещён в корзину.']

    if cur_path.is_dir():
        if '-r' not in opts:
            raise RmError('Это каталог. Добавь -r для рекурсивного удаления.')

        yorn = input(f'Удалить каталог {cur_path.name} (перемещение в корзину)? (y/n): ').strip().lower()
        if yorn != 'y':
            return ['Удаление отменено.']
        tr_path = _uniq_path_trash(cur_path)
        try:
            shutil.move(cur_path, tr_path)
        except PermissionError:
            raise RmError('Нет прав на удаление каталога.')
        except OSError as e:
            raise RmError(f'Ошибка удаления каталога {e}.')

        append_undo_rec({
            'op': 'rm',
            'old_path': str(cur_path),
            'new_path': str(tr_path),
            'is_dir': True,
            'time': datetime.datetime.now().strftime(ct.LOG_TIME_FORMAT),
        })
        return [f'Каталог {cur_path.name} перемещён в корзину.']

    raise RmError('Неподдерживаемый тип объекта.')


def command_cp(state, args: list[str], opts: set[str]) -> list[str]:
    '''
    Копирует файл или папку, -r - рекурсивное копирование для папок
    :param state: Объект состояния, в котором есть текущий путь
    :param args: Аргументы (например путь)
    :param opts: Опции типа -r итд
    :return: Список со строкой о копировании
    '''

    if len(args) < 2:
        raise CpError('Укажите текущий и новый пути.')

    raw_old, raw_new = args[0].strip(), args[1].strip()

    try:
        old = get_path(raw_old, state.cwd)
        new = get_path(raw_new, state.cwd)
    except Exception:
        raise CpError('Некорректный путь.')

    if not old.exists():
        raise CpError('Файл или каталог не существует.')

    if old.is_file():
        try:
            if new.is_dir():
                itog_new = new / old.name
            else:
                itog_new = new
            shutil.copy2(old, itog_new)
        except PermissionError:
            raise CpError('Нет прав на копирование файла.')
        except OSError as e:
            raise CpError(f'Ошибка копирование файла {e}.')
        append_undo_rec({
            'op': 'cp',
            'old_path': str(old),
            'new_path': str(itog_new),
            'is_dir': False,
            'time': datetime.datetime.now().strftime(ct.LOG_TIME_FORMAT),
        })
        return [f'Файл {old.name} скопирован в {new}.']

    if old.is_dir():
        if '-r' not in opts:
            raise CpError('Это каталог. Добавь -r для рекурсивного копирование.')
        try:
            if new.exists() and new.is_dir():
                itog_new = new / old.name
            else:
                itog_new = new
            shutil.copytree(old, itog_new, dirs_exist_ok=True)
        except PermissionError:
            raise CpError('Нет прав на копирование каталога.')
        except OSError as e:
            raise CpError(f'Ошибка копирование каталога {e}.')
        append_undo_rec({
            'op': 'cp',
            'old_path': str(old),
            'new_path': str(itog_new),
            'is_dir': True,
            'time': datetime.datetime.now().strftime(ct.LOG_TIME_FORMAT),
        })
        return [f'Каталога {old.name} скопирован в {new}.']

    raise CpError('Неподдерживаемый тип объекта.')


def command_mv(state, args: list[str], opts: set[str]) -> list[str]:
    '''
    Перемещает файл или папку, -r - рекурсивное перемещение для папок
    Также может переименовывать
    :param state: Объект состояния, в котором есть текущий путь
    :param args: Аргументы (например путь)
    :param opts: Опции типа -r итд
    :return: Список со строкой о перемещении
    '''

    if len(args) < 2:
        raise MvError('Укажите текущий и новый пути.')

    raw_old, raw_new = args[0].strip(), args[1].strip()

    try:
        old = get_path(raw_old, state.cwd)
        new = get_path(raw_new, state.cwd)
    except Exception:
        raise MvError('Некорректный путь.')

    if not old.exists():
        raise MvError('Файл или каталог не существует.')

    if old.is_file():
        try:
            if new.is_dir():
                itog_new = new / old.name
            else:
                if not new.parent.exists():
                    raise MvError('Каталог, в который перемещаем, не найден.')
                itog_new = new

            if new.exists():
                raise MvError('Объект с таким именем уже существует в месте, куда перемещаем.')

            shutil.move(old, new)
        except PermissionError:
            raise MvError('Нет прав на перемещение файла.')
        except OSError as e:
            raise MvError(f'Ошибка перемещение файла {e}.')
        append_undo_rec({
            'op': 'mv',
            'old_path': str(old),
            'new_path': str(itog_new),
            'is_dir': False,
            'time': datetime.datetime.now().strftime(ct.LOG_TIME_FORMAT),
        })
        return [f'Файл {old.name} перемещен в {new}.']

    if old.is_dir():
        try:
            if new.exists() and new.is_dir():
                itog_new = new / old.name
            else:
                if not new.parent.exists():
                    raise MvError('Каталог, в который перемещаем, не найден.')
                itog_new = new
            if new.exists():
                raise MvError('Объект с таким именем уже существует в месте, куда перемещаем.')
            shutil.move(old, new)
        except PermissionError:
            raise MvError('Нет прав на перемещение каталога.')
        except OSError as e:
            raise MvError(f'Ошибка перемещение каталога {e}.')
        append_undo_rec({
            'op': 'mv',
            'old_path': str(old),
            'new_path': str(itog_new),
            'is_dir': True,
            'time': datetime.datetime.now().strftime(ct.LOG_TIME_FORMAT),
        })
        return [f'Каталог {old.name} перемещен в {new}.']

    raise MvError('Неподдерживаемый тип объекта.')
