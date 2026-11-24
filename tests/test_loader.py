import pytest

from price_analysis.exceptions import MissingColumnError, PriceLoadError
from price_analysis.loaders import load_price_list
from tests.conftest import make_csv


def test_load_valid_csv(make_csv):
    path = make_csv("shop.csv", "sku,name,price\nA-1,Товар,100\nA-2,Товар2,200\n")
    result = load_price_list(path)
    assert len(result.records) == 2
    assert result.records["A-1"].price == 100


def test_missing_column_raises(make_csv):
    path = make_csv("bad.csv", "sku,name\nA-1,Товар\n")
    with pytest.raises(MissingColumnError):
        load_price_list(path)


def test_bad_price_raises(make_csv):
    path = make_csv("bad_price.csv", "sku,name,price\nA-1,Товар,abc\n")
    with pytest.raises(PriceLoadError) as exc_info:
        load_price_list(path)
    assert exc_info.value.row == 2


def test_unsupported_extension_raises(make_csv):
    path = make_csv("prices.json", "sku,name,price\nA-1,Товар,100\n")
    with pytest.raises(PriceLoadError):
        load_price_list(path)


def test_load_xlsx(tmp_path):
    import pandas as pd

    path = tmp_path / "comp.xlsx"
    pd.DataFrame([{"sku": "A-1", "name": "Товар", "price": 100}]).to_excel(path, index=False)

    result = load_price_list(path)
    assert result.records["A-1"].price == 100