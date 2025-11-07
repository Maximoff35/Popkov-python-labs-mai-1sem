import pytest
from pathlib import Path
from src import constants as ct
from src import store, plugins, state, fs
from src.errors import *
import zipfile
import tarfile


def change_constants():
    ct.BASE_DIR = Path('test_dir')
    ct.STORAGE_DIR = ct.BASE_DIR / 'storage'
    ct.LOG_FILE = ct.STORAGE_DIR / 'shell.log'
    ct.HISTORY_FILE = ct.STORAGE_DIR / '.history'
    ct.UNDO_FILE = ct.STORAGE_DIR / '.undo.json'
    ct.TRASH_DIR = ct.STORAGE_DIR / '.trash'
    ct.BASE_DIR.mkdir(parents=True, exist_ok=True)
    ct.STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    ct.TRASH_DIR.mkdir(parents=True, exist_ok=True)
    if not ct.HISTORY_FILE.exists():
        ct.HISTORY_FILE.touch()
    if not ct.UNDO_FILE.exists():
        ct.UNDO_FILE.write_text('[]', encoding='utf-8')
    store.init_storage()
    s = state.ShellState()
    s.cwd = ct.BASE_DIR
    return s


def test_command_history():
    s = change_constants()
    ct.HISTORY_FILE.write_text('', encoding='utf-8')
    store.history_append('ls')
    store.history_append('cd x')
    store.history_append('cat a.txt')
    out = plugins.command_history(s, [], set())
    assert out == ['1 ls', '2 cd x', '3 cat a.txt']
    out2 = plugins.command_history(s, ['2'], set())
    assert out2 == ['1 cd x', '2 cat a.txt']
    with pytest.raises(HistoryError):
        plugins.command_history(s, ['-3'], set())
    with pytest.raises(HistoryReadError):
        plugins.command_history(s, ['10'], set())


def test_command_zip_and_unzip():
    s = change_constants()
    d = s.cwd / 'zip_old'
    (d / 'aa').mkdir(parents=True, exist_ok=True)
    (d / 'aa' / 'z.txt').write_text('z', encoding='utf-8')
    zipka = s.cwd / 'zipka.zip'
    outz = plugins.command_zip(s, ['zip_old', 'zipka.zip'], set())
    assert zipka.exists()
    with zipfile.ZipFile(zipka, 'r') as z:
        names = z.namelist()
        assert any('zip_old/aa/z.txt' in n or 'aa/z.txt' in n for n in names)
    outu = plugins.command_unzip(s, ['zipka.zip'], set())
    assert (s.cwd / 'zip_old' / 'aa' / 'z.txt').exists()
    fs.command_rm(s, ['zipka.zip'], set())


def test_command_tar_and_untar():
    s = change_constants()
    d = s.cwd / 'tar_old'
    (d / 'bb').mkdir(parents=True, exist_ok=True)
    (d / 'bb' / 't.txt').write_text('t', encoding='utf-8')
    tarik = s.cwd / 'tarik.tar.gz'
    outt = plugins.command_tar(s, ['tar_old', 'tarik.tar.gz'], set())
    assert tarik.exists()
    with tarfile.open(tarik, 'r:gz') as t:
        names = t.getnames()
        assert any('tar_old/bb/t.txt' in n or 'bb/t.txt' in n for n in names)
    outu = plugins.command_untar(s, ['tarik.tar.gz'], set())
    assert (s.cwd / 'tar_old' / 'bb' / 't.txt').exists()
    fs.command_rm(s, ['tarik.tar.gz'], set())


def test_command_zip_errors():
    s = change_constants()
    with pytest.raises(ZipError):
        plugins.command_zip(s, ['only_one'], set())
    nd = s.cwd / 'not_dir'
    nd.write_text('x', encoding='utf-8')
    with pytest.raises(ZipError):
        plugins.command_zip(s, ['not_dir', 'x.zip'], set())


def test_command_unzip_errors():
    s = change_constants()
    with pytest.raises(UnzipError):
        plugins.command_unzip(s, [], set())
    f = s.cwd / 'notzip.txt'
    f.write_text('x', encoding='utf-8')
    with pytest.raises(UnzipError):
        plugins.command_unzip(s, ['notzip.txt'], set())


def test_command_tar_errors():
    s = change_constants()
    with pytest.raises(TarError):
        plugins.command_tar(s, ['only_one'], set())
    nd = s.cwd / 'not_dir2'
    nd.write_text('x', encoding='utf-8')
    with pytest.raises(TarError):
        plugins.command_tar(s, ['not_dir2', 'x.tar.gz'], set())


def test_command_untar_errors():
    s = change_constants()
    with pytest.raises(UntarError):
        plugins.command_untar(s, [], set())
    f = s.cwd / 'nottar.gz'
    f.write_text('x', encoding='utf-8')
    with pytest.raises(UntarError):
        plugins.command_untar(s, ['nottar.gz'], set())
