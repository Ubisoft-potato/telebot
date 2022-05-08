from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from ..items import RfiItem


class CnSpider(CrawlSpider):
    name = 'cn'
    allowed_domains = ['www.rfi.fr']
    start_urls = [
        'https://www.rfi.fr/cn/中国'
    ]
    rules = (
        Rule(LinkExtractor(restrict_css=(
            '.m-item-list-article.m-item-list-article--main-article',
            '.o-layout-list__item.l-m-100.l-t-50.l-d-50')),
            callback='parse_item',
            follow=False),
    )

    def parse_item(self, response):
        loader = ItemLoader(item=RfiItem(), response=response)
        loader.add_css('title', 'h1::text')
        loader.add_css('abstract', '.t-content__chapo::text')
        loader.add_value('url', response.url)
        item = loader.load_item()
        self.logger.info(item)
        yield item
