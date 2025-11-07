from pathlib import Path
from src import store
from src import fs
from src.state import ShellState
import shlex


def main() -> None:
    '''
    Точка входа.
    :return: Ничего не возвращает
    '''
    store.init_storage()
    state = ShellState()

    print('Мини-оболочка: введите "exit", чтобы выйти.')

    commands = {
        'ls': fs.command_ls,
        'cd': fs.command_cd,
        'cat': fs.command_cat,
        'rm': fs.command_rm,
        'cp': fs.command_cp,
        'mv': fs.command_mv,
    }

    while True:
        line = input(f'{state.cwd}> ').strip()

        if not line:
            continue
        if line == 'exit':
            print('Выход.')
            break
        store.history_append(line)

        name_command, args, opts = parse(line)

        if not name_command:
            continue

        if name_command not in commands:
            print(f'Неизвестная команда: {name_command}.')
            store.log_error(f'ERROR: {line} | Неизвестная команда: {name_command}.')
            continue

        try:
            res = commands[name_command](state, args, opts)
            if res:
                for row in res:
                    print(row)
            store.log_ok(line)
        except Exception as e:
            print(f'Ошибка: {e}')
            store.log_error(f'ERROR: {line} | {e}')


def parse(line: str) -> tuple[str, list[str], set[str]]:
    '''
    Разбивает строку пользователя на название команды, аргументы и опции.
    :param line: Ввод пользователя
    :return: Кортеж из названия, списка аргументов, списка опций
    '''

    tokens = shlex.split(line)

    if not tokens:
        return ('', [], set())
    name_command = tokens[0]
    ostalnoe = tokens[1:]
    opts = [i for i in ostalnoe if i != '' and i[0] == '-']
    args = [i for i in ostalnoe if i == '' or i[0] != '-']

    return (name_command, args, opts)


if __name__ == '__main__':
    main()
