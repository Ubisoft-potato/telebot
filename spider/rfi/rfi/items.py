# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


class RfiItem(scrapy.Item):
    title = scrapy.Field(output_processor=TakeFirst())
    abstract = scrapy.Field(input_processor=MapCompose(str.strip),
                            output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
