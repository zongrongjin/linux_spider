from scrapy import signals
from fake_useragent import UserAgent

class UAmiddleware(object):
    def __init__(self, spider_set):
        self.spider_set = spider_set

    @classmethod
    def from_crawler(cls, crawler):
        c = cls(crawler.settings['CHANGE_UA_SPIDERS'])
        crawler.signals.connect(c.spider_opened, signal=signals.spider_opened)
        return c

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
        
    def process_request(self, request, spider):
        if spider.name in self.spider_set:
            fake_ua = UserAgent().chrome
            request.headers['User-Agent'] = fake_ua
            spider.logger.debug('%s\'s user-agent become %s' % (spider.name, fake_ua))