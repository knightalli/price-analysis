from price_analysis.models import LoadResult, MatchedProduct
from price_analysis.loaders import load_price_list


def matching_products(own: LoadResult, competitors: dict[str, LoadResult]) -> tuple[list[MatchedProduct], set[str]]:
    """Делает список и цены продуктов нашего магазина, совпавших с продуктами магазинов конкурентов"""
    matched: list[MatchedProduct] = []
    unmatched: set[str] = set()

    for sku, record in own.records.items():
        prices = {
            name: comp.records[sku].price for name, comp in competitors.items() if sku in comp.records
        }
        if prices:
            matched.append(MatchedProduct(
                sku = sku,
                name = record.name,
                own_price = record.price,
                competitor_prices = prices,
            ))
        else:
            unmatched.add(sku)

    return matched, unmatched

if __name__ == "__main__":
    matched, unmatched = matching_products(
        load_price_list("../../data/shop.csv"),
        {"a": load_price_list("../../data/competitor_a.csv"),
         "b": load_price_list("../../data/competitor_b.xlsx")},
    )
    for m in matched: print(m.sku, m.own_price, m.competitor_prices)
    print("Без пары:", unmatched)