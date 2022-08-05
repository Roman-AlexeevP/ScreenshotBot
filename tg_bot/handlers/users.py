import asyncio
import dataclasses
import logging
from typing import Union
from urllib.parse import urlparse
from time import time

import aiogram.utils.markdown as fmt
from aiogram import Dispatcher
from aiogram import types
from pyppeteer import launch
from pyppeteer.errors import NetworkError

from validators.validate import validate_url

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class PageDetail:
    url: str
    screenshot: Union[bytes, str]
    title: str
    calculation_time_sec: int


async def user_start(message: types.Message):
    logger.info(f"User {message.from_user.id} start work with bot")
    message = "Привет! Меня зовут ImagerClone. Я - Бот для создания веб-скриншотов." \
              "\nЧтобы получить скриншот - отправьте URL адрес сайта. Например, wikipedia.org"

    await message.reply(message)


async def on_message(message: types.Message):
    temporary_message = await message.reply(fmt.bold("Запрос отправлен на сайт"))
    page_detail = await save_screenchot(message=message)
    text = fmt.text(
        fmt.text(f"{page_detail.title}"),
        fmt.text("Веб-сайт", page_detail.url, sep=": "),
        fmt.text("Время обработки", f"{page_detail.calculation_time_sec:.1f} сек.", sep=": "),
        sep="\n\n"
    )
    await temporary_message.delete()
    await message.answer_photo(photo=page_detail.screenshot,
                               caption=text,
                               parse_mode=types.ParseMode.HTML)


async def save_screenchot(message: types.Message) -> PageDetail:
    started_at = time()
    logger.info(f"URL: {message.text} from user: {message.from_user.id}")
    browser = await launch()
    page = await browser.newPage()
    url = validate_url(message.text)

    domain = urlparse(url).netloc
    try:
        await page.goto(url, waitUntil="networkidle2")
    except NetworkError as exc:
        logger.exception(exc)
        await message.answer("Неверная ссылка, попробуйте еще раз")
    else:
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


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(on_message, content_types=types.ContentType.TEXT)
