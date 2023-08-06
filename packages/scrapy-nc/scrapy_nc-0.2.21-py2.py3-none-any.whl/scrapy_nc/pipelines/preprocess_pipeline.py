from scrapy.exceptions import DropItem
import datetime

class PreprocessPipeline(object):

    def process_item(self, item, spider):
        unique_id = item.get('unique_id')
        if not unique_id:
            spider.logger.error(f'unique_id is None')
            raise DropItem('unique_id is None')
        if type(unique_id) == int:
            item['unique_id'] = str(unique_id)
        if type(unique_id) != str:
            spider.logger.error(f'unique_id type not str')
            raise DropItem('unique_id type not str')
        item['crawled_at'] = datetime.datetime.utcnow().replace(
            tzinfo=datetime.timezone.utc)
        return item
