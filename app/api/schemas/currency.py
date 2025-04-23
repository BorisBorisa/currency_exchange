from pydantic import BaseModel, Field
from typing import Annotated


class CurrencyPairConversion(BaseModel):
    base_currency: Annotated[str, Field(pattern="^[A-Z]{3}$")]
    target_currency: Annotated[str, Field(pattern="^[A-Z]{3}$")]
    amount: Annotated[float, Field(gt=0)]


class ConvertedCurrencyPair(CurrencyPairConversion):
    conversion_result: float