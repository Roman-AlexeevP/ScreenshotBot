from dataclasses import asdict

import pytest

from tg_bot.services import whois

@pytest.mark.asyncio
async def test_wrong_url_query():
    wrong_url = "https://lki.r"
    whois_info: whois.WhoisInfo = await whois.get_whois_response(wrong_url)
    assert isinstance(whois_info, whois.WhoisInfo)
    assert not whois_info.status
    assert whois_info.query == wrong_url

@pytest.mark.asyncio
async def test_right_whois_url_query():
    right_url = "lki.ru"
    whois_info: whois.WhoisInfo = await whois.get_whois_response(right_url)

    api_right_info = {
        "message": "-",
        "url": right_url,
        "query": "5.101.152.40",
        "status": True,
        "continent": "Europe",
        "country": "Russia",
        "regionName": "St.-Petersburg",
        "city": "St Petersburg",
        "isp": "Virtual hosting BEGET.RU",
        "org": "Beget Ltd"
    }
    assert asdict(whois_info) == api_right_info