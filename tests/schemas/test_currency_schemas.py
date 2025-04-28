import pytest
from pydantic import ValidationError
from app.api.schemas import currency


def test_valid_currency_pair_conversion():
    model = currency.CurrencyPairConversion(
        base_currency="USD",
        target_currency="EUR",
        amount=100.5)

    assert model.base_currency == "USD"
    assert model.target_currency == "EUR"
    assert model.amount == 100.5


@pytest.mark.parametrize("base", ["RUB", "KZT"])
@pytest.mark.parametrize("target", ["EUR", "USD"])
@pytest.mark.parametrize("amount", [1, 100.0, "1000"])
def test_currency_pair_accepts_valid_data(base, target, amount):
    currency.CurrencyPairConversion(
        base_currency=base,
        target_currency=target,
        amount=amount
    )


@pytest.mark.parametrize("base, target, amount", [
    ("RUB", "EU", 1),
    ("EU", "RUB", 1),
    ("EURO", "RUB", 2),
    ("RUB", "EURO", 2),
    ("rub", "EUR", 3),
    ("Rub", "EUR", 3),
    ("RUB", "eur", 3),
    ("RUB", "Eur", 3),
    ("RUB", "EUR", 0),
    ("RUB", "EUR", -10),
    (1.1, "EUR", 4),
    ("RUB", 1.2, 4),
    ("RUB", "EUR", "ABC"),

])
def test_currency_pair_rejects_invalid_data(base, target, amount):
    with pytest.raises(ValidationError):
        currency.CurrencyPairConversion(
            base_currency=base,
            target_currency=target,
            amount=amount
        )


def test_valid_converted_currency_pair():
    model = currency.ConvertedCurrencyPair(
        base_currency="USD",
        target_currency="EUR",
        amount=100.5,
        conversion_result=123.2
    )

    assert model.base_currency == "USD"
    assert model.target_currency == "EUR"
    assert model.amount == 100.5
    assert model.conversion_result == 123.2



