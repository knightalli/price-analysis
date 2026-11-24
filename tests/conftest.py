import pytest

@pytest.fixture
def make_csv(tmp_path):
    """Фикстура-фабрика для создания csv-файла"""
    def _make(name: str, text: str):
        p = tmp_path / name
        p.write_text(text, encoding="utf-8")
        return p
    return _make