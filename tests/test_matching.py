import pytest

from price_analysis.matching import matching_products
from price_analysis.models import LoadResult, PriceRecord


def _record(sku: str, price: float) -> PriceRecord:
    return PriceRecord(sku = sku, name = "Товар", price = price)


def test_exact_match():
    own = LoadResult(records = {"A-1": _record("A-1", 100)})
    comp = LoadResult(records = {"A-1": _record("A-1", 90)})

    matched, unmatched = matching_products(own, {"c1": comp})

    assert len(matched) == 1
    assert unmatched == set()
    assert matched[0].sku == "A-1"
    assert matched[0].competitor_prices == {"c1": 90}


def test_only_our_sku_goes_to_unmatched():
    own = LoadResult(records = {"A-1": _record("A-1", 100)})
    comp = LoadResult(records = {"B-2": _record("B-2", 50)})

    matched, unmatched = matching_products(own, {"c1": comp})

    assert matched == []
    assert unmatched == {"A-1"}


def test_sku_only_at_competitor_is_ignored():
    own = LoadResult(records = {"A-1": _record("A-1", 100)})
    comp = LoadResult(records = {"A-1": _record("A-1", 90),
                               "B-9": _record("B-9", 10)})

    matched, _ = matching_products(own, {"c1": comp})

    assert [m.sku for m in matched] == ["A-1"]


def test_prices_from_two_competitors_are_merged():
    own = LoadResult(records = {"A-1": _record("A-1", 100)})
    comp_a = LoadResult(records = {"A-1": _record("A-1", 90)})
    comp_b = LoadResult(records = {"A-1": _record("A-1", 95),
                                 "B-2": _record("B-2", 10)})

    matched, _ = matching_products(own, {"a": comp_a, "b": comp_b})

    assert matched[0].competitor_prices == {"a": 90, "b": 95}


def test_no_competitors_at_all():
    own = LoadResult(records = {"A-1": _record("A-1", 100)})

    matched, unmatched = matching_products(own, {})

    assert matched == []
    assert unmatched == {"A-1"}
