# -*- coding: utf-8 -*-

from scrapy.exceptions import DropItem
import pika
import os
import json
from scrapy_nc.queue.producer import Producer
class AMQPPipeline(object):
    def __init__(self,
                 mq_dev_user,
                 mq_dev_password,
                 mq_dev_host,
                 mq_dev_port,
                 mq_dev_vhost,
                 mq_prod_user,
                 mq_prod_password,
                 mq_prod_host,
                 mq_prod_port,
                 mq_prod_vhost):
        self.producer_dev = Producer(
            mq_dev_host, mq_dev_port, mq_dev_vhost, mq_dev_user, mq_dev_password)
        self.producer_prod = Producer(
            mq_prod_host, mq_prod_port, mq_prod_vhost, mq_prod_user, mq_prod_password)

    def process_item(self, item, spider):
        cralab_env = os.environ.get('CRAWLAB_ENV')
        if cralab_env == 'HK':
            return item
        queue_names = item.queue_names()
        if len(queue_names) == 0:
            spider.logger.info(
                f"queue name length is 0, item url {item.get('url')}")
            # raise DropItem(f"empty queue_name item {item.get('url')}")
            return item
        for queue_name in queue_names:
            tasks = []
            if queue_name.endswith('.dev'):
                tasks.append({
                    "env": "dev",
                    "queue_name": queue_name
                })
            elif queue_name.endswith('.prod'):
                tasks.append({
                    "env": "prod",
                    "queue_name": queue_name
                })
            else:
                tasks.append({
                    "env": "dev",
                    "queue_name": queue_name + '.dev'
                })
                tasks.append({
                    "env": "prod",
                    "queue_name": queue_name + '.prod'
                })
            for task in tasks:
                env = task['env']
                queue_name = task['queue_name']

                amqp_queue_use_item = spider.settings.get(
                    'AMQP_QUEUE_USE_ITEM')
                queue_data = {}
                if amqp_queue_use_item == True:
                    data = item
                    queue_data = data.to_json_str()
                else:
                    queue_data = json.dumps({
                        "filename": item.get('oss_filename'),
                        "channel": spider.name,
                        "source_id": item.get('unique_id'),
                        "url": item.get('url', default=''),
                    }, ensure_ascii=False)

                if env == 'dev':
                    try:
                        self.producer_dev.publish(queue_name, queue_data)
                    except:
                        pass
                else:
                    self.producer_prod.publish(queue_name, queue_data)
                    spider.logger.info(f"send to amqp {queue_name} item: {item['unique_id']}, url: {item.get('url', default='')}")
        return item

    def open_spider(self, spider):
        self.producer_dev.connect()
        self.producer_prod.connect()
        spider.logger.info(f'create channel success')

    def close_spider(self, spider):
        self.producer_dev.close()
        self.producer_prod.close()
        spider.logger.info(f'close connection success')

    @classmethod
    def from_crawler(cls, crawler):
        if crawler.spider is None:
            return
        mq_dev_user = crawler.spider.settings.get('MQ_DEV_USER') if crawler.spider.settings.get(
            'MQ_DEV_USER') else os.environ.get('MQ_DEV_USER')
        mq_dev_password = crawler.spider.settings.get('MQ_DEV_PASSWORD') if crawler.spider.settings.get(
            'MQ_DEV_PASSWORD') else os.environ.get('MQ_DEV_PASSWORD')
        mq_dev_host = crawler.spider.settings.get('MQ_DEV_HOST') if crawler.spider.settings.get(
            'MQ_DEV_HOST') else os.environ.get('MQ_DEV_HOST')
        mq_dev_port = crawler.spider.settings.get('MQ_DEV_PORT') if crawler.spider.settings.get(
            'MQ_DEV_PORT') else os.environ.get('MQ_DEV_PORT')
        mq_dev_vhost = crawler.spider.settings.get('MQ_DEV_VHOST') if crawler.spider.settings.get(
            'MQ_DEV_VHOST') else os.environ.get('MQ_DEV_VHOST')

        mq_prod_user = crawler.spider.settings.get('MQ_PROD_USER') if crawler.spider.settings.get(
            'MQ_PROD_USER') else os.environ.get('MQ_PROD_USER')
        mq_prod_password = crawler.spider.settings.get('MQ_PROD_PASSWORD') if crawler.spider.settings.get(
            'MQ_PROD_PASSWORD') else os.environ.get('MQ_PROD_PASSWORD')
        mq_prod_host = crawler.spider.settings.get('MQ_PROD_HOST') if crawler.spider.settings.get(
            'MQ_PROD_HOST') else os.environ.get('MQ_PROD_HOST')
        mq_prod_port = crawler.spider.settings.get('MQ_PROD_PORT') if crawler.spider.settings.get(
            'MQ_PROD_PORT') else os.environ.get('MQ_PROD_PORT')
        mq_prod_vhost = crawler.spider.settings.get('MQ_PROD_VHOST') if crawler.spider.settings.get(
            'MQ_PROD_VHOST') else os.environ.get('MQ_PROD_VHOST')

        return cls(
            mq_dev_user,
            mq_dev_password,
            mq_dev_host,
            mq_dev_port,
            mq_dev_vhost,
            mq_prod_user,
            mq_prod_password,
            mq_prod_host,
            mq_prod_port,
            mq_prod_vhost
        )
