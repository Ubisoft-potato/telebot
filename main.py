#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import datetime

import log

import pytz
from loguru import logger
from redis import Redis
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from config import settings
from handler.job import BotJob
from handler.message import BotMessage
from handler.shodan_operation import ShodanOperation
from handler.usage import *


def get_cron_users(redis: Redis) -> list:
    """
    Get all users from cron.
    """
    return redis.lrange("telebot:users", 0, -1)


def telegram_bot() -> None:
    """
    Start the bot.
    """
    # Create the Updater and pass it your bot's token.
    updater = Updater(token=settings["token"])

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    shodan_operation = ShodanOperation()
    redis = Redis(host=settings["redis"]["host"],
                  port=settings["redis"]["port"],
                  db=settings["redis"]["db"],
                  decode_responses=True)

    bot_msg = BotMessage(shodan_operation, redis)
    bot_job = BotJob(redis)

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("jetbrains", bot_msg.get_jetbrains_license_servers))
    dispatcher.add_handler(CallbackQueryHandler(bot_msg.daily_feed_callback))

    for uid in get_cron_users(redis):
        logger.info(f"Registering Daily Feed User: {uid}")
        updater.job_queue.run_once(bot_job.rfi_daily_push, when=1, context=uid)
        updater.job_queue.run_daily(bot_job.rfi_daily_push,
                                    time=datetime.time(hour=8, minute=0, tzinfo=pytz.timezone("Asia/Shanghai")),
                                    days=(0, 1, 2, 3, 4, 5, 6),
                                    context=uid)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    log.init_log_conf()
    telegram_bot()
