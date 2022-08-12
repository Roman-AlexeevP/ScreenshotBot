from aiogram.utils import markdown as fmt

from services import screenshots, whois


def get_user_start_text() -> str:
    text = fmt.text(
        fmt.text("Привет! Меня зовут ImagerClone. Я - Бот для создания веб-скриншотов."),
        fmt.text("Чтобы получить скриншот - отправьте URL адрес сайта."),
        fmt.text("Например, http://wikipedia.org"),
        sep="\n\n"
    )
    return text


def get_screenshot_caption(page_detail: screenshots.PageDetail):
    text = fmt.text(
        fmt.text(f"{page_detail.title}"),
        fmt.text(f"Веб-сайт: {page_detail.url}"),
        fmt.text(f"Время обработки: {page_detail.calculation_time_sec:.1f} сек."),
        sep="\n\n"
    )
    return text


def get_error_whois_text(whois_info: whois.WhoisInfo) -> str:
    text = fmt.text(
        fmt.text(f"URL: {whois_info.url}"),
        fmt.text(f"Статус: {whois_info.status}"),
        fmt.text(f"Текст ошибки: {whois_info.message}"),
        sep="\n\n"
    )
    return text


def get_whois_text(whois_info: whois.WhoisInfo) -> str:
    text = fmt.text(
        fmt.text(f"IP: {whois_info.query}"),
        fmt.text(f"Страна: {whois_info.country}"),
        fmt.text(f"Континент: {whois_info.continent}"),
        fmt.text(f"Город: {whois_info.city}"),
        fmt.text(f"Провайдер: {whois_info.isp}"),
        fmt.text(f"Организация: {whois_info.org}"),
        sep="\n\n"
    )
    return text


def get_wrong_url_text() -> str:
    text = fmt.text(
        fmt.text("Неправильная ссылка или формат. Попробуйте еще раз, пример ссылки:"),
        fmt.text(r"https://github.com"),
        sep="\n"
    )
    return text
