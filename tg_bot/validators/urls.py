import aiohttp

import consts


async def check_url_status(url: str) -> bool:
    """
    Check url response code
    Good response codes: 2xx, 3xx
    """
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                status = response.status
        except (aiohttp.InvalidURL, aiohttp.ClientConnectorError):
            return False
        else:
            return status in consts.VALIDE_RESPONSE_STASUSES