from telegram.parsemode import ParseMode
from telegram.ext import CallbackContext

from redis import Redis

from .rfi.feed import generate_daily_feed


class BotJob:

    def __init__(self, redis: Redis):
        self.redis = redis

    def rfi_daily_push(self, context: CallbackContext):
        rfi_feed, keyboard = generate_daily_feed(self.redis, 1)
        if rfi_feed and keyboard:
            context.bot.send_message(chat_id=context.job.context,
                                     text=rfi_feed,
                                     parse_mode=ParseMode.MARKDOWN,
                                     reply_markup=keyboard)

        else:
            context.bot.send_message(chat_id=context.job.context,
                                     text="Rfi Daily Push No Content Scraped")
