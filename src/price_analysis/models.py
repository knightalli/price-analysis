from pydantic import BaseModel, Field


class PriceRecord(BaseModel):
    sku: str = Field(min_length = 1)
    name: str
    price: float = Field(gt = 0)
    cost: float | None = Field(default=None, gt=0)
    source: str = ""


class LoadResult(BaseModel):
    records: dict[str, PriceRecord] = {}
    warnings: list[str] = []


class MatchedProduct(BaseModel):
    sku: str
    name: str
    own_price: float
    cost: float | None = Field(default=None, gt=0)
    competitor_prices: dict[str, float] = {}


class AnalysedProduct(BaseModel):
    sku: str
    name: str
    own_price: float
    min_competitor_price: float
    median_competitor_price: float
    gap_pct: float
    status: str
    below_cost: bool
    recommended_price: float
    reason: str