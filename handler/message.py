from telegram.utils import helpers
from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from .shodan_operation import ShodanOperation
from loguru import logger

shodanOperation = ShodanOperation()

# shodan search query
jetbrains_license_server = 'Location: https://account.jetbrains.com/fls-auth'


def get_jetbrains_license_servers(update: Update, context: CallbackContext) -> None:
    """
    Get the JetBrains license servers.
    """
    rsp = shodanOperation.search(jetbrains_license_server)
    bot_message = '*JetBrains license servers*\n'
    for result in rsp["matches"]:
        hostnames = result["hostnames"]
        if len(hostnames) > 0:
            bot_message += f'**Host:** {helpers.escape_markdown(hostnames[0], version=2)}\n' \
                           f'**Org:** _{helpers.escape_markdown(result["org"], version=2)}_\n\n'

    update.message.reply_markdown_v2(text=bot_message)
