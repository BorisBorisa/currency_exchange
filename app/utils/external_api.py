import httpx
import json
import asyncio

from config import ERAPI_settings
from app.api.schemas.currency import CurrencyPairConversion, ConvertedCurrencyPair


async def get_conversion_rates(base_code: str):
    async with httpx.AsyncClient() as client:
        api_response = await client.get(f"{ERAPI_settings.BASE_URL}/"
                                        f"{ERAPI_settings.API_KEY}/latest/"
                                        f"{base_code}")

        conversion_rates = json.loads(api_response.text)["conversion_rates"]

    return conversion_rates

async def get_pair_conversion_result(conversion_pair: CurrencyPairConversion) -> ConvertedCurrencyPair:
    async with httpx.AsyncClient() as client:
        api_response = await client.get(f"{ERAPI_settings.BASE_URL}/"
                                        f"{ERAPI_settings.API_KEY}/pair/"
                                        f"{conversion_pair.base_currency}/"
                                        f"{conversion_pair.target_currency}/"
                                        f"{conversion_pair.amount}")

        return ConvertedCurrencyPair(
            **conversion_pair.model_dump(),
            conversion_result=json.loads(api_response.text)["conversion_result"]
        )


if __name__ == "__main__":
    print(ERAPI_settings.API_KEY)
    print(ERAPI_settings.BASE_URL)
    # print(asyncio.run(get_conversion_rates("RUB")))

    tmp_pair = CurrencyPairConversion(base_currency="RUB", target_currency="USD", amount=100000)

    print(asyncio.run(get_pair_conversion_result(tmp_pair)))