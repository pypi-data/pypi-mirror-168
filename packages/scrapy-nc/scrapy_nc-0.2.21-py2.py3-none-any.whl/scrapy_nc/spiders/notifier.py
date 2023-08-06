import scrapy
import requests


class NotifierSpider(scrapy.Spider):
    def parse(self, response):
        pass

    name = 'notifier'
    notified = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # default method, you can override this method to change the default rules
    def notify(self, stats):
        return stats.get('item_scraped_count', 0) < 1

    def closed(self, reason):
        self._notify()

    def _notify(self):
        # {'downloader/exception_count': 1,
        #  'downloader/exception_type_count/twisted.internet.error.TimeoutError': 1,
        #  'downloader/request_bytes': 197438,
        #  'downloader/request_count': 510,
        #  'downloader/request_method_count/GET': 510,
        #  'downloader/response_bytes': 12368745,
        #  'downloader/response_count': 509,
        #  'downloader/response_status_count/200': 411,
        #  'downloader/response_status_count/301': 7,
        #  'downloader/response_status_count/302': 53,
        #  'downloader/response_status_count/404': 2,
        #  'downloader/response_status_count/429': 6,
        #  'downloader/response_status_count/500': 30,
        #  'dupefilter/filtered': 170,
        #  'elapsed_time_seconds': 267.276458,
        #  'finish_reason': 'finished',
        #  'finish_time': datetime.datetime(2020, 7, 17, 7, 34, 38, 810636),
        #  'httperror/response_ignored_count': 12,
        #  'httperror/response_ignored_status_count/404': 2,
        #  'httperror/response_ignored_status_count/500': 10,
        #  'item_scraped_count': 129,
        #  'log_count/ERROR': 10,
        #  'log_count/INFO': 10414,
        #  'log_count/WARNING': 107,
        #  'memusage/max': 134623232,
        #  'memusage/startup': 64512000,
        #  'request_depth_max': 1,
        #  'response_received_count': 422,
        #  'retry/count': 27,
        #  'retry/max_reached': 10,
        #  'retry/reason_count/429 Unknown Status': 6,
        #  'retry/reason_count/500 Internal Server Error': 20,
        #  'retry/reason_count/twisted.internet.error.TimeoutError': 1,
        #  'scheduler/dequeued': 510,
        #  'scheduler/dequeued/memory': 510,
        #  'scheduler/enqueued': 510,
        #  'scheduler/enqueued/memory': 510,
        #  'start_time': datetime.datetime(2020, 7, 17, 7, 30, 11, 534178)}
        if self.notified:
            return
        stats = self.crawler.stats.get_stats()
        log_warn = stats.get('log_count/WARNING', 0)
        log_error = stats.get('log_count/ERROR', 0)
        items = stats.get('item_scraped_count', 0)
        if self.notify(stats):
            self.notified = True
            requests.post(
                'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=adefa3a5-57f9-42b2-a52e-d3fa32717732',
                json={
                    "msgtype": "text",
                    "text": {
                        "content": f"spider [{self.name}] triggered the alarm\r\n\r\nitem count: {items}\r\n"
                                   f"log warn count: {log_warn}\r\nlog error count: {log_error}"
                    }
                },
                timeout=10,
            )
            self.logger.info(f"send notify to wechat work success")
