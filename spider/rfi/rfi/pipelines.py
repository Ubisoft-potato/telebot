# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import time

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from redis import Redis

import uuid
from datetime import datetime


class RfiPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('abstract') is None:
            raise DropItem(f'Missing abstract in {item.get("title")}')
        return item


class RedisRfiPipeline:
    redis: Redis = None

    def __init__(self, redis_host, redis_port, redis_db):
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_db = redis_db
        self.date = datetime.today().strftime('%Y%m%d')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            redis_host=crawler.settings.get('REDIS_HOST'),
            redis_port=crawler.settings.get('REDIS_PORT'),
            redis_db=crawler.settings.get('REDIS_DB')
        )

    def open_spider(self, spider):
        self.redis = Redis(host=self.redis_host, port=self.redis_port, db=self.redis_db)
        spider.logger.info(f'Connected to Redis on {self.redis_host}:{self.redis_port}, Ping: {self.redis.ping()}')

    def close_spider(self, spider):
        self.redis.expire(f'rfi:docs:{self.date}', 86400)
        self.redis.close()

    def process_item(self, item, spider):
        rfi_item = ItemAdapter(item).asdict()
        doc_id = uuid.uuid1()
        fields = self.redis.hset(f'rfi:{doc_id.int}', mapping=rfi_item)
        spider.logger.info(f'Rfi Item Info: {rfi_item["title"]} Saved To Redis : {fields > 0}')
        self.redis.expire(f'rfi:{doc_id.int}', 86400)
        self.redis.rpush(f'rfi:docs:{self.date}', doc_id.int)
