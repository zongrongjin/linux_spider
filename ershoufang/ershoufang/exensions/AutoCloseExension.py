import logging
import time
from scrapy import signals
from scrapy.exceptions import NotConfigured

logger = logging.getLogger(__name__)

class AutoCloseExension(object):
    def __init__(self, crawler, idle_num):
        self.crawler = crawler
        self.idle_num = idle_num
        self.idle_counter = 0
        self.idle_list = []

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('MYEXT_ENABLED', True):
            raise NotConfigured

        idle_number = crawler.settings.getint('AUTO_CLOSE_TIME', 1800) // 5

        ext = cls(idle_number, crawler)

        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.spider_idle, signal=signals.spider_idle)

        return ext

    def spider_opened(self, spider):
        logger.info("opened spider %s redis spider Idle, Continuous idle limit： %d", spider.name, self.idle_num)

    def spider_closed(self, spider):
        logger.info("closed spider %s, idle counter %d , Continuous idle count %d",
                    spider.name, self.idle_counter, len(self.idle_list))

    def spider_idle(self, spider):
        self.idle_counter += 1                      
        self.idle_list.append(time.time())      
        idle_list_len = len(self.idle_list)        

        if idle_list_len > 2 and self.idle_list[-1] - self.idle_list[-2] > 6:
            self.idle_list = [self.idle_list[-1]]

        elif idle_list_len > self.idle_num:
            logger.info('\n continued idle number exceed {} Times'
                        '\n meet the idle shutdown conditions, will close the reptile operation'
                        '\n idle start time: {},  close spider time: {}'.format(self.idle_num,
                                                                              self.idle_list[0], self.idle_list[0]))
            self.crawler.engine.close_spider(spider, 'closespider_pagecount')