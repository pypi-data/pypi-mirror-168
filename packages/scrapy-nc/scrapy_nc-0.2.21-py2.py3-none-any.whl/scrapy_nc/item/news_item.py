import scrapy
import json
from scrapy_nc.item import BaseItem


class NewsItem(BaseItem):
    url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    html = scrapy.Field()
    picture = scrapy.Field()
    summary = scrapy.Field()
    publish_date = scrapy.Field()
    crawled_date = scrapy.Field()
    language = scrapy.Field()
    channel = scrapy.Field()
    source_type = scrapy.Field()
    source = scrapy.Field()
    extra = scrapy.Field()
    rule = scrapy.Field()
    message_package = scrapy.Field()

    def to_dict(self):
        dt = self.__dict__['_values']
        # del rule data before serialize
        dt.pop('rule', '')
        dt.pop('message_package', '')
        return dt

    def to_json_str(self):
        if self.get('publish_date') is not None:
            self['publish_date'] = self['publish_date'].isoformat()
        if self['crawled_date'] is not None:
            self['crawled_date'] = self['crawled_date'].isoformat()
        return json.dumps(self.to_dict(), ensure_ascii=False)
