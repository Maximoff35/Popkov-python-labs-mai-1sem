import pytest
from src import constants as ct
from pathlib import Path
from src import store, state
from src import fs
from src.errors import *
import json
from src import plugins


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


def test_get_path():
    s = change_constants()
    baza = s.cwd
    p1 = fs.get_path(None, baza)
    p2 = fs.get_path('', baza)
    p3 = fs.get_path('.', baza)
    assert p1 == baza
    assert p2 == baza
    assert p3 == baza
    absdir = (baza / 'qwe').resolve()
    p4 = fs.get_path(str(absdir), baza)
    assert p4 == absdir
    p5 = fs.get_path('aha/ahaha.txt', baza)
    assert str(p5).endswith(str(Path('test_dir') / 'aha' / 'ahaha.txt'))


def test_command_ls():
    s = change_constants()
    papka = s.cwd / 'lsik'
    papka.mkdir(parents=True, exist_ok=True)
    (papka / 'd1').mkdir(exist_ok=True)
    (papka / 'a.txt').write_text('x', encoding='utf-8')
    out = fs.command_ls(s, ['lsik'], set())
    assert 'a.txt' in out
    assert 'd1/' in out
    out_l = fs.command_ls(s, ['lsik'], {'-l'})
    assert all('|' in row for row in out_l)
    with pytest.raises(LsError):
        fs.command_ls(s, ['ahahaha'], set())
    pfile = (papka / 'a.txt')
    with pytest.raises(LsError):
        fs.command_ls(s, [str(pfile)], set())


def test_command_cd():
    s = change_constants()
    d = s.cwd / 'cdik'
    d.mkdir(exist_ok=True)
    out = fs.command_cd(s, ['cdik'], set())
    assert s.cwd == d.resolve()
    f = d / 'f.txt'
    f.write_text('x', encoding='utf-8')
    with pytest.raises(CdError):
        fs.command_cd(s, ['f.txt'], set())
    with pytest.raises(CdError):
        fs.command_cd(s, ['dich'], set())


def test_command_cat():
    s = change_constants()
    d = s.cwd / 'catik'
    d.mkdir(exist_ok=True)
    f = d / 'a.txt'
    f.write_text('l1\nl2', encoding='utf-8')
    out = fs.command_cat(s, ['catik/a.txt'], set())
    assert out == ['l1', 'l2']
    with pytest.raises(CdError):
        fs.command_cat(s, ['catik'], set())
    with pytest.raises(CatError):
        fs.command_cat(s, ['catik/dich.txt'], set())


def test_command_rm_and_undo():
    s = change_constants()
    f = s.cwd / 'rmik.txt'
    f.write_text('hello', encoding='utf-8')
    out = fs.command_rm(s, ['rmik.txt'], set())
    assert 'перемещ' in ''.join(out)
    assert not f.exists()
    assert any(p.name[:4] == 'rmik' and p.name[-4:] == '.txt' for p in ct.TRASH_DIR.iterdir())
    data = json.loads(ct.UNDO_FILE.read_text(encoding='utf-8'))
    assert data and data[-1]['op'] == 'rm'
    out2 = plugins.command_undo(s, [], set())
    assert 'восстановлен' in ''.join(out2)
    assert f.exists()


def test_command_rm_r_dir(monkeypatch):
    s = change_constants()
    d = s.cwd / 'rmrik'
    (d / 'papkarmr').mkdir(parents=True, exist_ok=True)
    (d / 'papkarmr' / 'x.txt').write_text('1', encoding='utf-8')
    monkeypatch.setattr('builtins.input', lambda _: 'y')
    out = fs.command_rm(s, ['rmrik'], {'-r'})
    assert 'перемещ' in ''.join(out)
    assert not d.exists()
    assert any(p.name[:5] == 'rmrik' for p in ct.TRASH_DIR.iterdir())


def test_command_cp():
    s = change_constants()
    f = s.cwd / 'cp_old.txt'
    f.write_text('data', encoding='utf-8')
    fs.command_cp(s, ['cp_old.txt', 'cp_new.txt'], set())
    assert (s.cwd / 'cp_new.txt').exists()
    d = s.cwd / 'cp_dir'
    (d / 'papka').mkdir(parents=True, exist_ok=True)
    (d / 'papka' / 'a.txt').write_text('1', encoding='utf-8')
    fs.command_cp(s, ['cp_dir', 'cp_dir_copy'], {'-r'})
    assert (s.cwd / 'cp_dir_copy' / 'papka' / 'a.txt').exists()
    with pytest.raises(CpError):
        fs.command_cp(s, ['ahahahah', 'x'], set())


def test_command_mv_and_undo():
    s = change_constants()

    f_old = s.cwd / 'mv_old.txt'
    f_old.write_text('m', encoding='utf-8')
    fs.command_mv(s, ['mv_old.txt', 'mv_new.txt'], set())
    assert not (s.cwd / 'mv_old.txt').exists()
    assert (s.cwd / 'mv_new.txt').exists()

    (s.cwd / 'mv_old1.txt').write_text('m', encoding='utf-8')
    with pytest.raises(MvError):
        fs.command_mv(s, ['mv_old1.txt', 'mv_new.txt'], set())

    out_u1 = plugins.command_undo(s, [], set())
    assert 'восстановлен' in ''.join(out_u1).lower()
    assert (s.cwd / 'mv_old.txt').exists()
    assert not (s.cwd / 'mv_new.txt').exists()

    d_old = s.cwd / 'mv_dir'
    (d_old / 'k').mkdir(parents=True, exist_ok=True)
    (d_old / 'k' / 'q.txt').write_text('1', encoding='utf-8')
    fs.command_mv(s, ['mv_dir', 'mv_dir_new'], set())
    assert not (s.cwd / 'mv_dir').exists()
    assert (s.cwd / 'mv_dir_new' / 'k' / 'q.txt').exists()
    out_u2 = plugins.command_undo(s, [], set())
    assert 'восстановлен' in ''.join(out_u2).lower()
    assert (s.cwd / 'mv_dir' / 'k' / 'q.txt').exists()
    assert not (s.cwd / 'mv_dir_new').exists()

    with pytest.raises(MvError):
        fs.command_mv(s, ['sskjdbfgui', 'ewfkjnbeiuwsrgbuiyb'], set())


def test_command_rm_errors():
    s = change_constants()
    with pytest.raises(RmError):
        fs.command_rm(s, [], set())
    with pytest.raises(RmError):
        fs.command_rm(s, ['/'], set())
    with pytest.raises(RmError):
        fs.command_rm(s, ['..'], set())
    with pytest.raises(RmError):
        fs.command_rm(s, ['sdkjhfjdsiubgfiusdb'], set())
