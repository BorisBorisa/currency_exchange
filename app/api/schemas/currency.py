from pydantic import BaseModel, Field


class CurrencyPairConversion(BaseModel):
    base_currency: str = Field(pattern="^[A-Z]{3}$", example="RUB")
    target_currency: str= Field(pattern="^[A-Z]{3}$", example="USD")
    amount: float = Field(gt=0)