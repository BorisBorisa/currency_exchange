import httpx
import json

from fastapi import HTTPException, status
from httpx import TimeoutException, HTTPError, Response
from config import ERAPI_settings
from app.api.schemas.currency import CurrencyPairConversion, ConvertedCurrencyPair


async def get_api_response(url: str) -> Response:
    async with httpx.AsyncClient() as client:
        try:
            api_response = await client.get(url, timeout=3)

        except TimeoutException:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Превышено время ожидания. Попробуйте позже."
            )

        except HTTPError:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Ошибка запроса к внешнему API"
            )

        if api_response.status_code == 500:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail={"error-type": api_response.json()["error-type"]}
            )

        return api_response



async def get_conversion_rates(base_code: str):
    api_response = await get_api_response(
        f"{ERAPI_settings.BASE_URL}/"
        f"{ERAPI_settings.API_KEY}/latest/"
        f"{base_code}"
    )

    conversion_rates = json.loads(api_response.text)["conversion_rates"]
    return conversion_rates


async def get_pair_conversion_result(conversion_pair: CurrencyPairConversion) -> ConvertedCurrencyPair:
    api_response = await get_api_response(
        f"{ERAPI_settings.BASE_URL}/"
        f"{ERAPI_settings.API_KEY}/pair/"
        f"{conversion_pair.base_currency}/"
        f"{conversion_pair.target_currency}/"
        f"{conversion_pair.amount}"
    )

    return ConvertedCurrencyPair(
        **conversion_pair.model_dump(),
        conversion_result=json.loads(api_response.text)["conversion_result"]
    )


if __name__ == "__main__":
    pass
