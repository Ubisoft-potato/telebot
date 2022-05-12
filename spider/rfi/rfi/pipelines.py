# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class RfiPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('abstract') is None:
            raise DropItem(f'Missing abstract in {item.get("title")}')
        spider.logger.info(f'Processing {item}')
        return item
