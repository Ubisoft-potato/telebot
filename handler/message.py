from telegram.utils import helpers
from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from redis import Redis
from loguru import logger

from .shodan_operation import ShodanOperation
from .rfi.feed import generate_daily_feed


class BotMessage:
    shodanOperation: ShodanOperation = None
    redis: Redis = None

    jetbrains_license_server = 'Location: https://account.jetbrains.com/fls-auth'

    def __init__(self, shodan_operation: ShodanOperation, redis: Redis):
        self.shodanOperation = shodan_operation
        self.redis = redis

    def get_jetbrains_license_servers(self, update: Update, context: CallbackContext) -> None:
        """
        Get the JetBrains license servers.
        """
        rsp = self.shodanOperation.search(self.jetbrains_license_server)
        bot_message = '*JetBrains license servers*\n'
        for result in rsp["matches"]:
            hostnames = result["hostnames"]
            port = result["port"]
            if len(hostnames) > 0:
                bot_message += f'**Host:** {helpers.escape_markdown(hostnames[0], version=2)}:{port}\n' \
                               f'**Org:** _{helpers.escape_markdown(result["org"], version=2)}_\n\n'

        update.message.reply_markdown_v2(text=bot_message)

    def daily_feed_callback(self, update: Update, context: CallbackContext) -> None:
        """
        Get the daily feed.
        """
        query = update.callback_query
        query.answer()
        rfi_feed, keyboard = generate_daily_feed(self.redis, int(query.data))
        if rfi_feed and keyboard:
            query.edit_message_text(text=rfi_feed,
                                    parse_mode=ParseMode.MARKDOWN,
                                    reply_markup=keyboard)
