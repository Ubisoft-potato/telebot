from telegram import Update, ForceReply
from telegram.ext import CallbackContext


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """
    Send a message when the command /start is issued.
    """
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!')
