
from price_analysis.analysis import analyze_product
from price_analysis.models import MatchedProduct
from price_analysis.rules import PricingRules


def _matched(own, comp_prices, cost=None):
    return MatchedProduct(sku="A-1", name="Т", own_price=own,
                          cost=cost, competitor_prices=comp_prices)


def test_recommendation_follows_median_not_dumper():
    p = analyze_product(_matched(100, {"a": 96, "b": 88, "c": 95}), PricingRules())
    assert p.status == "dumping"
    assert p.median_competitor_price == 95
    assert p.recommended_price == 93.1


def test_market_down_when_majority_below():
    p = analyze_product(_matched(100, {"a": 80, "b": 82, "c": 96}), PricingRules())
    assert p.status == "market_down"


def test_dont_chase_competitor_below_floor():
    p = analyze_product(_matched(100, {"c": 50}, cost=80), PricingRules())
    assert p.recommended_price == 88.0
    assert "минимума" in p.reason


def test_market_up_raises_price():
    p = analyze_product(_matched(80, {"c": 100}), PricingRules())
    assert p.status == "market_up"
    assert p.recommended_price == 98.0
