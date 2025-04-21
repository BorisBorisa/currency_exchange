import httpx
import json
import asyncio

from app.utils.config import ERAPI_settings


async def get_conversion_rates(base_code: str):
    async with httpx.AsyncClient() as client:
        api_response = await client.get(f"{ERAPI_settings.BASE_URL}/{ERAPI_settings.API_KEY}/latest/{base_code}")
        conversion_rates = json.loads(api_response.text)["conversion_rates"]

    return conversion_rates


if __name__ == "__main__":
    print(ERAPI_settings.API_KEY)
    print(ERAPI_settings.BASE_URL)
    print(asyncio.run(get_conversion_rates("RUB")))

