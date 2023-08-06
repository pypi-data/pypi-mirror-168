import os
import requests
import json


class ProxyDownloaderMiddleware(object):

    def __init__(self, proxy_server_addr):
        self.proxy_server_addr = proxy_server_addr

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        proxy_server_addr = crawler.spider.settings.get('PROXY_SERVER_ADDR') if crawler.spider.settings.get(
            'PROXY_SERVER_ADDR') else os.environ.get('PROXY_SERVER_ADDR')
        s = cls(proxy_server_addr)
        return s

    def process_request(self, request, spider):
        if request.meta.get('skip_proxy') == True:
            return None
        req_url = request.url
        if 'splash' in request.meta:
            req_url = request.meta['splash']['args']['url']
        proxy = self.get_proxy(request, spider.name, req_url)
        if proxy is not None:
            if proxy['pass'] is not None and proxy['pass'] != '':
                proxy_server = f"http://{proxy['user']}:{proxy['pass']}@{proxy['host']}:{proxy['port']}"
            else:
                proxy_server = f"http://{proxy['host']}:{proxy['port']}"

            if 'splash' in request.meta:
                request.meta['splash']['args']['proxy'] = proxy_server
            else:
                request.meta['proxy'] = proxy_server
                request.headers["Proxy-Authorization"] = proxy['basic_auth_header']

        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest

        headers = request.headers
        proxy_try_count = self.get_proxy_try_count_from_request(request)
        if response.status != 200 and proxy_try_count < 10:
            headers["Proxy_Try_Count"] = str(proxy_try_count)
            headers["Proxy_URL"] = self.get_proxy_from_request(request)
            request.replace(headers=headers)
            return request

        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def get_proxy(self, request, name, url):
        proxy_try_count = request.headers.get('Proxy_Try_Count')
        proxy_url = request.headers.get('Proxy_URL')
        try:
            response = requests.get(self.proxy_server_addr + f"/get?name={name}&url={url}", timeout=10,
                                    headers={"proxy_try_count": proxy_try_count, "proxy_url": proxy_url})
        except Exception as err:
            print(f'get proxy error occurred: {err}, spider name: {name}, request url: {url}')
            return None

        resp = response.json()

        return {
            'host': resp['host'],
            'user': resp['user'],
            'pass': resp['pass'],
            'port': resp['port'],
            'type': resp['type'],
            'basic_auth_header': resp['basic_auth_header'],
        }

    def get_proxy_from_request(self, request):
        if 'splash' in request.meta:
            return request.meta['splash']['args']['proxy'];
        else:
            return request.meta['proxy']

    def get_proxy_try_count_from_request(self, request):
        headers = request.headers
        if headers.get('Proxy_Try_Count') is None:
            proxy_try_count = 1
        else:
            proxy_try_count = int(headers.get('Proxy_Try_Count'))
            proxy_try_count += 1

        return proxy_try_count
