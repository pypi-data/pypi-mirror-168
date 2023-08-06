from scrapy.exceptions import DropItem
import requests
import os
import json
import time
import traceback
from scrapy.utils.serialize import ScrapyJSONEncoder
encoder = ScrapyJSONEncoder()

headers = {'Content-Type': "application/json"}

class FlowPipeline(object):

    def process_item(self, item, spider):
        unique_id = item.get('unique_id')
        if not unique_id:
            raise DropItem('unique_id is None')

        data = item.deepcopy().to_dict()

        crawled_at = data.get('crawled_at')
        if crawled_at:
            data['crawled_at'] = data['crawled_at'].isoformat()

        data = json.loads( encoder.encode(data))

        # convert datetime to str before serialize
        flow_urls = item.get('flow_urls', None)
        if not flow_urls:
            flow_urls = spider.settings.get('FLOW_URLS')
        if flow_urls:
            data_helper_url = spider.settings.get('DATA_HELPER_URL')
            if not data_helper_url:
                data_helper_url = os.environ.get('DATA_HELPER_URL')
            config_type = type(flow_urls)
            flows = []
            if config_type == str:
                flows.append(flow_urls)
            elif config_type == list:
                flows = flow_urls
            else:
                spider.logger.error(f'flow urls config type error, make sure the type must be an array or string')
                return item
            
            for i in range(10):
                if spider.settings.get("DISABLE_DATA_HELPER") is True:
                    for flow_url in flows:
                        try:
                            response = requests.post(flow_url, data = json.dumps(data,ensure_ascii=False).encode('utf8'), timeout=10,headers = headers)
                            if int(response.status_code) == 200:
                                spider.logger.info(f'req addr: {flow_url}  {unique_id} request success new')
                            else:
                                spider.logger.info(f'req addr: {flow_url} {unique_id} request fail, {response.status_code} {data}')
                        except:
                            traceback.print_exc()
                            spider.logger.warn(f'send data to flow fail, try times: {i} : {item.get("unique_id")} {flow_url}')
                            time.sleep(3)
                    return item
                else:
                    try:
                        response = requests.post(data_helper_url, json={
                            'flow_urls': flows,
                            'payload': json.dumps(data,ensure_ascii=False).encode('utf-8'),
                        }, timeout=5)
                        if response.status_code == 200:
                            spider.logger.info(f'send data to helper success: {item.get("unique_id")} {data_helper_url} {flows}')
                            return item
                        else:
                            spider.logger.warn(f'send data to helper fail: {item.get("unique_id")} {data_helper_url} {flows} {response.status_code}')
                    except:
                        spider.logger.warn(f'send data to helper fail, try times: {i} : {item.get("unique_id")} {data_helper_url} {flows}')
                        time.sleep(3)
        return item

