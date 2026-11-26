from pydantic import BaseModel, Field


class PricingRules(BaseModel):
    """Бизнес-правила ценообразования. Указываются в долях"""

    min_margin: float = Field(default = 0.10, ge = 0, le = 1)
    """Минимальная наценка к себестоимости"""

    dumping_threshold: float = Field(default = 0.1, ge = 0, le = 1)
    """Величина, показывающая, на сколько может быть меньше конкурент, чтобы определить демпинг или понижение рынка"""

    max_drop: float = Field(default=0.10, ge=0, le=1)
    """Максимальное снижение от собственной цены"""

    market_down_share: float = Field(default=0.6, ge=0, le=1)
    """Доля конкурентов дешевле нас, при которой это тренд рынка"""

    undercut_step: float = Field(default=0.02, ge=0, le=1)
    """На сколько подрезать медианную цену конкурентов."""