import logging

from aiogram import Dispatcher
from aiogram import types

import consts
from db.managers import UserHistoryManager
from keyboard import whois_keybord_factory, callback_factory
from services import screenshots
from services import whois
from tg_bot import text_factory
from tg_bot.validators import urls

logger = logging.getLogger(__name__)


async def user_start(message: types.Message):
    logger.info(f"User {message.from_user.id} start work with bot")
    await message.reply(text_factory.get_user_start_text())


async def on_message(message: types.Message, manager: UserHistoryManager):
    logger.info(f"URL: {message.text} from user: {message.from_user.id}")

    is_url_correct = await urls.check_url_status(message.text)
    if not is_url_correct:
        logger.warning(f"Wrong URL:{message.text} from user: {message.from_user.id}")
        await manager.log_action(user_id=message.from_user.id,
                                 url=message.text,
                                 success=False)
        return await message.reply(text_factory.get_wrong_url_text(), disable_web_page_preview=True)

    temp_photo = types.InputFile(path_or_bytesio=f"{consts.MEDIA_DIR_NAME}loading.png")
    temporary_message = await message.answer_photo(photo=temp_photo, caption="Запрос отправлен на сайт")

    page_detail = await screenshots.save_screenchot(message=message)

    photo = types.InputMediaPhoto(media=types.InputFile(page_detail.screenshot_path),
                                  caption=text_factory.get_screenshot_caption(page_detail))

    keyboard = whois_keybord_factory(page_detail.url)
    await manager.log_action(user_id=message.from_user.id,
                             url=page_detail.url,
                             success=True)
    await temporary_message.edit_media(media=photo, reply_markup=keyboard)


async def whois_callback(call: types.CallbackQuery, callback_data: dict):
    url = callback_data["url"]
    logger.info(f"Get WHOIS URL: {url} from user: {call.from_user.id}")
    whois_info = await whois.get_whois_response(url)
    if not whois_info.status:
        await call.answer(text_factory.get_error_whois_text(whois_info), show_alert=True)
    await call.answer(text_factory.get_whois_text(whois_info), show_alert=True)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(on_message, content_types=types.ContentType.TEXT)
    dp.register_callback_query_handler(whois_callback, callback_factory.filter())
