import typing
import aiohttp
import faust
from loguru import logger
from ..app import app
from apps.collect_securities.services import AlphaVantageClient
from .. import records
from config import config as main_config
from database.cruds import SecurityCRUD


collect_security_overview_topic = app.topic(
    "collect_security_overview",
    internal=True,
    value_type=records.CollectSecurityOverview,
)


@app.agent(collect_security_overview_topic)
async def collect_security_overview(
    stream: faust.StreamT[records.CollectSecurityOverview],
) -> typing.AsyncIterable[bool]:
    async with aiohttp.ClientSession() as session:
        async for event in stream:
            logger.info(
                "Start collect security [{symbol}] overview",
                symbol=event.symbol
            )

            client = AlphaVantageClient(session, main_config.API_KEY)

            security_overview = await client.get_security_overview(
                event.symbol
            )

            await SecurityCRUD.update_one(
                {"symbol": event.symbol, "exchange": event.exchange},
                security_overview,
            )

            yield True