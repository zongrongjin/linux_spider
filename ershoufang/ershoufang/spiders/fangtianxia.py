# -*- coding: utf-8 -*-
import scrapy
import re
import logging
from urllib.parse import urljoin
from ershoufang.utils import *
from ershoufang.items import FangtianxiaItem
from scrapy_redis.spiders import RedisSpider


class FangtianxiaSpider(RedisSpider):
    name = 'fangtianxia'
    allowed_domains = ['fang.com']
    # start_urls = ['https://gz.esf.fang.com/newsecond/esfcities.aspx']
    redis_key = 'fangtianxia:start_urls'


    def parse(self, response):
        city_list = set(re.findall(r'//.{2,20}\.esf\.fang\.com', response.text))
        for city_url in city_list:
            if 'ld' not in city_list:
                yield  scrapy.Request(
                    url='https:' + city_url,
                    callback=self.parse_choose_price
                )
    
    def parse_choose_price(self, response):
        if is_full(response.text):
            logging.debug(response.url + '当前页面有100页数据，需要进一步筛选以获取更多数据')
            choose_list = response.css('.screen_box .floatl')
            price_type = choose_list[1].css('a::attr(href)').extract()
            for price_url in price_type:
                next_url = urljoin(response.url, price_url)
                yield scrapy.Request(
                    url=next_url,
                    callback=self.parse_choose_housetype
                )
        else:
            self.parse_page(response)

    def parse_choose_housetype(self, response):
        if is_full(response.text):
            logging.debug(response.url + '当前页面有100页数据，需要进一步筛选以获取更多数据')
            choose_list = response.css('.screen_box .floatl')
            house_type = choose_list[2].css('a::attr(href)').extract()
            for house_url in house_type:
                next_url = urljoin(response.url, house_url)
                yield scrapy.Request(
                    url=next_url,
                    callback=self.parse_choose_house_area
                )
        else:
            self.parse_page(response)

    def parse_choose_house_area(self, response):
        if is_full(response.text):
            logging.debug(response.url + '当前页面有100页数据，需要进一步筛选以获取更多数据')
            choose_list = response.css('.screen_box .floatl')
            area_type = choose_list[3].css('a::attr(href)').extract()
            for area_url in area_type:
                next_url = urljoin(response.url, area_url)
                yield scrapy.Request(
                    url=next_url,
                    callback=self.parse_page
                )
        else:
            self.parse_page(response)

    def parse_page(self, response):
        if is_empty(response.text):
            logging.debug(response.url + '当前页面无数据')
            return
        else:
            logging.debug(response.url + '获取当前页面房屋详情页')
            self.parse_house(response)
            next_page = response.css('span.on~p a::attr(href)').extract()
            if next_page is not None:
                next_page_url = urljoin(response.url, next_page)
                yield scrapy.Request(
                    url=next_page_url,
                    callback=self.parse_page
                )

    def parse_house(self, response):
        house_list = response.css('h4 a::attr(href)').extract()
        for house in house_list:
            house_url = urljoin(response.url, house)
            yield scrapy.Request(
                url=house_url,
                callback=self.parse_detail
            )

    def parse_detail(self, response):
        logging.debug(response.url + '获取房屋详情')
        item = FangtianxiaItem()
        item['house_room'] = response.css('h1::text').extract_first().strip()
        item['total_price'] = response.css('.zf_mianji b::text').extract_first()
        item['average_price'] = re.findall(r'\d{,6}元/平米', response.text)[0]
        yield item
