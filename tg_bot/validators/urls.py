import consts


def validate_protocol(url: str) -> str:
    """
    Check protocol for right work of page.goto() method
    """
    if not url.startswith(consts.PROTOCOL_HTTP) and not url.startswith(consts.PROTOCOL_HTTPS):
        url = consts.PROTOCOL_HTTP + url
    return url
