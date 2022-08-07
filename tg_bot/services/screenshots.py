import asyncio
import dataclasses
import logging
from time import time
from typing import Union
from urllib.parse import urlparse

from aiogram import types
from pyppeteer import launch
from pyppeteer.errors import NetworkError

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class PageDetail:
    url: str
    screenshot: Union[bytes, str]
    title: str
    calculation_time_sec: int


async def save_screenchot(message: types.Message) -> PageDetail:
    started_at = time()
    browser = await launch(
        executablePath="/usr/bin/google-chrome-stable",
        headless=True,
        args=["--no-sandbox"],
    )
    page = await browser.newPage()
    url = message.text

    domain = urlparse(url).netloc

    await page.goto(url, waitUntil="networkidle2")

    title = await page.title()
    path = f"{message.date:%Y_%m_%d}_{message.from_user.id}_{domain}.png"
    await page.setViewport({"width": 1920, "height": 1080})
    screenshot = await asyncio.wait_for(page.screenshot({
        "type": "jpeg",
        "quality": 100,
        "width": 1920,
        "height": 1080,
    }), timeout=30.0)
    await browser.close()

    return PageDetail(
        url=url,
        screenshot=screenshot,
        title=title,
        calculation_time_sec=time() - started_at
    )
