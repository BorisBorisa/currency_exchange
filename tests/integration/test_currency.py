import pytest
from pytest_mock import MockFixture
from httpx import Response, TimeoutException, HTTPError

EXCHANGE_CURRENCIES_REQUEST_BODY = {
    "base_currency": "RUB",
    "target_currency": "USD",
    "amount": 1000
}

EXCHANGE_CURRENCIES_RESPONSE = {
    "result": "success",
    "documentation": "https://www.exchangerate-api.com/docs",
    "terms_of_use": "https://www.exchangerate-api.com/terms",
    "time_last_update_unix": 1747267202,
    "time_last_update_utc": "Thu, 15 May 2025 00:00:02 +0000",
    "time_next_update_unix": 1747353602,
    "time_next_update_utc": "Fri, 16 May 2025 00:00:02 +0000",
    "base_code": "RUB",
    "target_code": "USD",
    "conversion_rate": 0.01244,
    "conversion_result": 12.44
}

EXCHANGE_CURRENCY_RATES_RESPONSE = {
    "result": "success",
    "documentation": "https://www.exchangerate-api.com/docs",
    "terms_of_use": "https://www.exchangerate-api.com/terms",
    "time_last_update_unix": 1747353601,
    "time_last_update_utc": "Fri, 16 May 2025 00:00:01 +0000",
    "time_next_update_unix": 1747440001,
    "time_next_update_utc": "Sat, 17 May 2025 00:00:01 +0000",
    "base_code": "RUB",
    "conversion_rates": {
        "RUB": 1,
        "EUR": 0.01114,
        "USD": 0.01247,
    }
}

EXCHANGE_CURRENCIES_ERROR_RESPONSE = {
    "result": "error",
    "error-type": "unknown-code"
}


@pytest.mark.asyncio
async def test_exchange_currencies_route(
        client,
        mocker: MockFixture,
        override_get_current_active_user
):
    mocker.patch(
        "app.utils.external_api.httpx.AsyncClient.get",
        return_value=Response(200, json=EXCHANGE_CURRENCIES_RESPONSE)
    )

    response = client.post("/currency/exchange", json=EXCHANGE_CURRENCIES_REQUEST_BODY)

    assert response.status_code == 200
    assert EXCHANGE_CURRENCIES_REQUEST_BODY.items() <= response.json().items()
    assert "conversion_result" in response.json()


@pytest.mark.asyncio
async def test_exchange_currency_rates(
        client,
        mocker: MockFixture,
        override_get_current_active_user
):
    mocker.patch(
        "app.utils.external_api.httpx.AsyncClient.get",
        return_value=Response(200, json=EXCHANGE_CURRENCY_RATES_RESPONSE)
    )

    response = client.get("/currency/rates", params={"base_currency": "RUB"})

    assert response.status_code == 200
    assert response.json() == EXCHANGE_CURRENCY_RATES_RESPONSE["conversion_rates"]


@pytest.mark.asyncio
async def test_exchange_currencies_list(
        client,
        override_get_current_active_user
):
    with client:
        response = client.get("/currency/list")

    assert response.status_code == 200
    assert len(response.json()) == 163


@pytest.mark.asyncio
async def test_exchange_currencies_route_timeout(
        client,
        mocker: MockFixture,
        override_get_current_active_user
):
    mocker.patch(
        "app.utils.external_api.httpx.AsyncClient.get",
        side_effect=TimeoutException("")
    )

    response = client.post("/currency/exchange", json=EXCHANGE_CURRENCIES_REQUEST_BODY)

    assert response.status_code == 504
    assert response.json()["detail"] == "Превышено время ожидания. Попробуйте позже."


@pytest.mark.asyncio
async def test_exchange_currencies_route_external_api_error(
        client,
        mocker: MockFixture,
        override_get_current_active_user
):
    mocker.patch(
        "app.utils.external_api.httpx.AsyncClient.get",
        side_effect=HTTPError("")
    )

    response = client.post("/currency/exchange", json=EXCHANGE_CURRENCIES_REQUEST_BODY)

    assert response.status_code == 502
    assert response.json()["detail"] == "Ошибка запроса к внешнему API"


@pytest.mark.asyncio
async def test_exchange_currencies_route_api_response_error(
        client,
        mocker: MockFixture,
        override_get_current_active_user
):
    mocker.patch(
        "app.utils.external_api.httpx.AsyncClient.get",
        return_value=Response(500, json=EXCHANGE_CURRENCIES_ERROR_RESPONSE)
    )

    response = client.post("/currency/exchange", json=EXCHANGE_CURRENCIES_REQUEST_BODY)

    assert response.status_code == 502
    assert "unknown-code" in response.text
