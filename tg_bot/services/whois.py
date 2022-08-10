import dataclasses
import logging

import aiohttp

from tg_bot import consts

logger = logging.getLogger(__name__)


@dataclasses.dataclass(frozen=True)
class WhoisInfo:
    url: str
    query: str
    status: bool
    message: str = "-"
    country: str = "-"
    continent: str = "-"
    regionName: str = "-"
    city: str = "-"
    isp: str = "-"
    org: str = "-"


async def get_whois_response(url: str) -> WhoisInfo:
    async with aiohttp.ClientSession() as session:
        api_url = f"{consts.WHOIS_API_URL}{url}"
        params = f"{consts.WHOIS_API_FIELDS_PARAMETER}={','.join(consts.WHOIS_API_FIELDS)}"
        try:
            async with session.get(api_url, params=params) as response:
                whois_info_json = await response.json()

        except (aiohttp.InvalidURL, aiohttp.ClientConnectorError):
            logger.error(f"Error while connected to API {api_url} with url {url}")
            return WhoisInfo(url=url, status=False, query=url, message="Ошибка в подключении к сервису по получению WHOIS")
        else:
            if whois_info_json.pop("status") == "fail":
                return WhoisInfo(url=url, status=False, query=url,
                                 message=whois_info_json["message"])
            return WhoisInfo(url=url, status=True, **whois_info_json)
