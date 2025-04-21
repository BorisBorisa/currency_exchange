from fastapi import APIRouter, Depends, Query
from asyncpg import Connection

from typing import Annotated

from app.core.security import get_current_active_user
from app.utils.external_api import get_conversion_rates

from db.db_connecion import get_database_connection
from db.queries import get_supported_currencies

from app.api.schemas.currency import CurrencyPairConversion

currency = APIRouter(prefix="/currency", dependencies=[Depends(get_current_active_user)])


@currency.get("/list")
async def get_currencies_list(conn: Connection = Depends(get_database_connection)):
    currencies: dict = await get_supported_currencies(conn)
    return currencies


@currency.get("/rates")
async def get_rates(base_currency: Annotated[str, Query(pattern="^[A-Z]{3}$")]):
    conversion_rates = await get_conversion_rates(base_currency)
    return conversion_rates


@currency.post("/exchange")
async def exchange_currencies(conversion_pair: CurrencyPairConversion):
    return conversion_pair
