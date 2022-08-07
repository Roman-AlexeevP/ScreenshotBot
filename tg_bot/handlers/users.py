import logging

import aiogram.utils.markdown as fmt
from aiogram import Dispatcher
from aiogram import types

from services.screenshots import save_screenchot
from tg_bot.validators import urls

logger = logging.getLogger(__name__)





async def user_start(message: types.Message):
    logger.info(f"User {message.from_user.id} start work with bot")
    message_text = "Привет! Меня зовут ImagerClone. Я - Бот для создания веб-скриншотов." \
              "\nЧтобы получить скриншот - отправьте URL адрес сайта. Например, wikipedia.org"

    await message.reply(message_text)


async def on_message(message: types.Message):
    logger.info(f"URL: {message.text} from user: {message.from_user.id}")
    is_url_correct = await urls.check_url_status(message.text)
    if not is_url_correct:
        logger.warning(f"Wrong URL:{message.text} from user: {message.from_user.id}")
        return await message.reply("Неправильная ссылка или формат. Попробуйте еще раз, пример ссылки:"
                                   r"https://github.com", disable_web_page_preview=True)
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



def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(on_message, content_types=types.ContentType.TEXT)
