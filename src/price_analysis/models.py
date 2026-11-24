from pydantic import BaseModel, Field


class PriceRecord(BaseModel):
    sku: str = Field(min_length = 1)
    name: str
    price: float = Field(gt = 0)
    source: str = ""

class LoadResult(BaseModel):
    records: dict[str, PriceRecord] = {}
    warnings: list[str] = []

class MatchedProduct(BaseModel):
    sku: str
    name: str
    own_price: float
    competitor_prices: dict[str, float] = {}