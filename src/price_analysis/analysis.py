import statistics

from price_analysis.models import MatchedProduct, AnalysedProduct
from price_analysis.rules import PricingRules


def analyze_product(matched: MatchedProduct, rules: PricingRules) -> AnalysedProduct:
    """Анализ продукта, который есть у конкурентов"""
    min_comp = min(matched.competitor_prices.values())
    gap = (matched.own_price - min_comp)/matched.own_price

    prices = list(matched.competitor_prices.values())
    med = statistics.median(prices)

    threshold_price = matched.own_price * (1 - rules.dumping_threshold)
    share_below = sum(p < threshold_price for p in matched.competitor_prices.values()) / len(matched.competitor_prices)

    if share_below > rules.market_down_share and len(matched.competitor_prices) > 1:
        status = "market_down"
    elif share_below > 0 or (matched.cost is not None and min_comp < matched.cost):
        status = "dumping"
    elif med > matched.own_price:
        status = "market_up"
    else:
        status = "normal"

    below_cost = matched.cost is not None and matched.own_price < matched.cost

    if matched.cost is not None:
        floor = matched.cost * (1 + rules.min_margin)
    else:
        floor = matched.own_price * (1 - rules.max_drop)
    raw = med * (1 - rules.undercut_step)

    recommended = max(raw, floor)

    if recommended > matched.own_price:
        if matched.cost is not None and floor > matched.own_price:
            reason = "Цена ниже минимальной маржи, надо увеличить цену"
        else:
            reason = "Рынок поднялся, надо увеличить цену"
    elif recommended < matched.own_price:
        if raw < floor:
            reason = "Цена конкурента ниже допустимого минимума"
        else:
            reason = "Рынок упал, надо уменьшить цену"
    else:
        reason = "Цена адекватна, предложено небольшое изменение"


    return AnalysedProduct(
        sku = matched.sku,
        name = matched.name,
        own_price = matched.own_price,
        min_competitor_price = min_comp,
        median_competitor_price = med,
        gap_pct = round(gap, 4),
        status = status,
        below_cost = below_cost,
        recommended_price = recommended,
        reason = reason,
    )


def analyze(matched: list[MatchedProduct], rules: PricingRules | None = None) -> list[AnalysedProduct]:
    rules = rules or PricingRules()
    return [analyze_product(product, rules) for product in matched]