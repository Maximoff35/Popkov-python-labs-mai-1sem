import logging
import pytest
from src import log
from src.simulation import run_simulation


def test_simulyaciya_krivoe_kolichestvo_shagov_tip():
    with pytest.raises(ValueError):
        run_simulation("10")


@pytest.mark.parametrize("krivoe_kolichestvo", [0, -1, 5, 9])
def test_simulyaciya_krivoe_kolichestvo_shagov_znachenie(krivoe_kolichestvo):
    with pytest.raises(ValueError):
        run_simulation(krivoe_kolichestvo)


def test_simulyaciya_krivoe_seed_tip():
    with pytest.raises(ValueError):
        run_simulation(10, seed="ne_celoe")


def test_simulyaciya_log_sozdaetsya_i_chto_to_pishetsya(tmp_path, monkeypatch):
    test_log = tmp_path / "test_shell.log"
    monkeypatch.setattr(log, "LOG_FILE", test_log, raising=False)
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    run_simulation(steps=10, seed=42)
    assert test_log.exists()
    soderzhimoe = test_log.read_text(encoding="utf-8")
    assert "==== СТАРТ СИМУЛЯЦИИ ====" in soderzhimoe
    assert "==== КОНЕЦ СИМУЛЯЦИИ ====" in soderzhimoe
    assert "[Шаг " in soderzhimoe
