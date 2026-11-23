import pytest

from price_analysis.exceptions import MissingColumnError, PriceLoadError
from price_analysis.loaders import load_price_list


def test_load_valid_csv(tmp_path):
    path = tmp_path / "shop.csv"
    path.write_text("sku,name,price\nA-1,Товар,100\nA-2,Товар2,200\n", encoding="utf-8")
    result = load_price_list(path)
    assert len(result.records) == 2
    assert result.records["A-1"].price == 100


def test_missing_column_raises(tmp_path):
    path = tmp_path / "bad.csv"
    path.write_text("sku,name\nA-1,Товар\n", encoding="utf-8")
    with pytest.raises(MissingColumnError):
        load_price_list(path)


def test_bad_price_raises(tmp_path):
    path = tmp_path / "bad_price.csv"
    path.write_text("sku,name,price\nA-1,Товар,abc\n", encoding="utf-8")
    with pytest.raises(PriceLoadError) as exc_info:
        load_price_list(path)
    assert exc_info.value.row == 2