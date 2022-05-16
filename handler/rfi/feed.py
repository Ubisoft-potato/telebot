from redis import Redis
from telegram.utils.helpers import escape_markdown
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger

from datetime import datetime
from typing import Tuple, Optional

page_size = 3


def generate_daily_feed(redis: Redis, current_page: int) -> Tuple[Optional[str], Optional[InlineKeyboardMarkup]]:
    date = datetime.today().strftime('%Y%m%d')
    docs = redis.lrange(f'rfi:docs:{date}', (current_page - 1) * page_size, current_page * page_size - 1)
    if len(docs) > 0:
        pipeline = redis.pipeline(transaction=False)
        for doc_id in docs:
            pipeline.hgetall(f'rfi:{doc_id}')
        res = pipeline.execute()
        rfi_feed = '*Radio France Internationale*\n'
        for doc in res:
            rfi_feed += f'[{doc["title"]}]({doc["url"]})\n' \
                        f'     {doc["abstract"]}\n\n'

        keyboard = []
        line = []
        doc_size = redis.llen(f'rfi:docs:{date}')
        pages = int(doc_size / page_size)
        logger.debug(f'Rfi Doc size: {pages}')
        if doc_size > pages * page_size:
            pages += 2
        else:
            pages += 1
        for page in range(1, pages):
            if page == current_page:
                line.append(InlineKeyboardButton(text=f'👀 {page}', callback_data=page))
            else:
                line.append(InlineKeyboardButton(text=f'{page}', callback_data=page))
            if len(line) == page_size:
                keyboard.append(line.copy())
                line.clear()
        keyboard.append(line)
        reply_markup = InlineKeyboardMarkup(keyboard)

        return rfi_feed, reply_markup
    else:
        return None, None
