import logging
from typing import Optional
from linebot import LineBotApi
from linebot.models import TextSendMessage


def setup_logger(
    log_file_name: Optional[str] = None, line_channel_access_token: Optional[str] = None
):
    l = logging.getLogger()

    if l.hasHandlers():
        return

    formatter = logging.Formatter(
        "%(asctime)s| %(message)s", datefmt="%d/%b/%Y-%H:%M:%S"
    )
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    l.addHandler(streamHandler)

    if log_file_name is not None:
        fileHandler = logging.FileHandler(log_file_name, mode="a")
        fileHandler.setFormatter(formatter)
        l.addHandler(fileHandler)
    if line_channel_access_token is not None:
        lineHandler = LineBotHandler(line_channel_access_token)
        # lineHandler.setFormatter(formatter)
        l.addHandler(lineHandler)

    l.setLevel("INFO")


def log(msg: str):
    l = logging.getLogger()
    l.info(msg)


class LineBotHandler(logging.Handler):
    def __init__(self, channel_access_token):
        logging.Handler.__init__(self)
        self.line_bot = LineBotApi(channel_access_token)

    def emit(self, record):
        msg = self.format(record)
        self.line_bot.broadcast(TextSendMessage(msg))
