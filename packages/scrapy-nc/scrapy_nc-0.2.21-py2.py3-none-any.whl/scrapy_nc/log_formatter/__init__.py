
from scrapy.logformatter import LogFormatter
import logging
import os

class DefaultLogFormatter(LogFormatter):
    def dropped(self, item, exception, response, spider):
        return {
            'level': logging.INFO,
            'msg': u"Dropped: %(exception)s" + os.linesep,
            'args': {
                'exception': exception,
                'item': item,
            },
        }


default_log_formatter = 'scrapy_nc.log_formatter.DefaultLogFormatter'
