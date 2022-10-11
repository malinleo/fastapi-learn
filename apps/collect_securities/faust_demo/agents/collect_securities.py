from ..app import app
import typing
from faust import StreamT
import aiohttp
from loguru import logger
from apps.collect_securities.services import AlphaVantageClient
from config import config as main_config
from database.cruds import SecurityCRUD
from .collect_security_overview import collect_security_overview
from .. import records

collect_securities_topic = app.topic(
    "collect_securities",
    internal=True,
)


@app.agent(collect_securities_topic)
async def collect_securities(
    stream: StreamT[None],
) -> typing.AsyncIterable[bool]:
    """Collect securities from API."""
    async with aiohttp.ClientSession() as session:
        async for _ in stream:
            logger.info("Start collect securities")

            client = AlphaVantageClient(session, main_config.API_KEY)

            securities = await client.get_securities()

            for security in securities:
                await SecurityCRUD.update_one(
                    {
                        "symbol": security["symbol"],
                        "exchange": security["exchange"],
                    },
                    security,
                    upsert=True,
                )

                await collect_security_overview.cast(
                    records.CollectSecurityOverview(
                        symbol=security["symbol"],
                        exchange=security["exchange"],
                    )
                )

            yield True
