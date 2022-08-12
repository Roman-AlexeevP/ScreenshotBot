import dataclasses
import logging
from datetime import datetime
from pathlib import Path
from time import time
from urllib.parse import urlparse

from aiogram import types
from pyppeteer import launch

import consts

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class PageDetail:
    url: str
    screenshot_path: Path
    title: str
    calculation_time_sec: float


def get_file_path(root_dir: Path, message_date: datetime, user_id, url) -> Path:
    domain = urlparse(url).netloc
    file_name = f"{consts.MEDIA_DIR_NAME}{message_date:%Y_%m_%d_%H_%M_%S}_{user_id}_{domain}.png"
    return root_dir / file_name


async def save_screenchot(message: types.Message) -> PageDetail:
    started_at = time()
    browser = await launch(
        executablePath="/usr/bin/google-chrome-stable",
        headless=True,
        ignoreHTTPSErrors=True,
        args=["--no-sandbox",
              '--ignore-certificate-errors',
              '--ignore-certificate-errors-spki-list',
              '--enable-features=NetworkService'
              ],
    )
    page = await browser.newPage()
    url = message.text

    await page.goto(url, waitUntil="networkidle2")

    title = await page.title()
    path = get_file_path(message.bot["root_dir"], message.date, message.from_user.id, url)
    await page.setViewport({"width": 1920, "height": 1080})
    await page.screenshot({
        "path": path,
        "type": "jpeg",
        "quality": 100,
        "width": 1920,
        "height": 1080,
    })
    await browser.close()

    return PageDetail(
        url=url,
        screenshot_path=path,
        title=title,
        calculation_time_sec=time() - started_at
    )
