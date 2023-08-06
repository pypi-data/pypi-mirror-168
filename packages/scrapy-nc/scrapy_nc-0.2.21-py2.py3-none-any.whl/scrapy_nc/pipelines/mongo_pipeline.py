from scrapy_nc.db import mongo_db
import json
from scrapy.exceptions import DropItem


class MongoPipeline(object):
    def process_item(self, item, spider):
        my_item = item.deepcopy()
        item_dict = dict(my_item)
        unique_id = item['unique_id']
        if not unique_id:
            raise DropItem('unique_id is None')

        crawled_at = item['crawled_at']
        if not crawled_at:
            raise DropItem('crawled_at is None')

        spider.collection.update_one({
            'unique_id': my_item.get('unique_id')
        }, {"$set": item_dict}, upsert=True)
        return item

    def open_spider(self, spider):
        pass

    @classmethod
    def from_crawler(cls, crawler):
        spider = crawler.spider
        instance = cls()
        if not mongo_db:
            spider.logger.error('mongodb no configuration')
            return instance
        collection_name = crawler.spider.settings.get('COLLECTION_NAME') if crawler.spider.settings.get(
            'COLLECTION_NAME') else spider.name
        spider.collection = mongo_db.get_collection(collection_name)
        res = json.dumps(spider.collection.index_information())
        spider.logger.info(
            f'index_information {res}')
        index_name = 'unique_id'
        if index_name not in spider.collection.index_information():
            spider.collection.create_index(
                'unique_id', unique=True, name=index_name)
            spider.logger.info(f"create unique index {index_name}")
        ttl = spider.settings.get('DATA_TTL')
        expire_index_name = "crawled_at"
        # 如果没有配置数据的过期时间，默认是永久有效
        if ttl is None:
            # 删除掉 这个字段的 索引信息， 让数据永久有效
            MongoPipeline.drop_index(spider, spider.collection, expire_index_name)
            spider.logger.info(f'not found data_ttl, the data is permanently valid')
        # 配置 -1， 也是永久有效
        elif ttl == -1:
            # 删除掉 这个字段的 索引信息， 让数据永久有效
            MongoPipeline.drop_index(spider, spider.collection, expire_index_name)
            # spider.collection.drop_index(expire_index_name)
            return instance
        elif ttl > 0:
            # ttl 大于0， 给数据创建一个自动过期的索引
            expire_index_name = "crawled_at"
            if expire_index_name not in spider.collection.index_information():
                spider.collection.create_index(
                    "crawled_at", name=expire_index_name, expireAfterSeconds=ttl,
                )
                spider.logger.info(f'create ttl index {expire_index_name}, ttl: {ttl}')
        return instance

    @staticmethod
    def drop_index(spider, collection, index_name):
        # 删除掉 这个字段的 索引信息， 让数据永久有效
        try:
            collection.drop_index(index_name)
        except Exception as e:
            spider.logger.warn(f"drop index response error: {e}")
        else:
            spider.logger.info(f"drop index: {index_name} success")
