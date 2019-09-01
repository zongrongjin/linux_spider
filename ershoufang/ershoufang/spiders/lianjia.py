# -*- coding: utf-8 -*-
import json
import re
import scrapy
import logging
from scrapy_redis.spiders import RedisSpider
from ershoufang.items import LianjiaItem
from scrapy.exceptions import CloseSpider


class LianjiaSpider(RedisSpider):
    name = 'lianjia'
    allowed_domains = ['lianjia.com']
    redis_key = 'lianjia:start_urls'

    def parse(self, response):
        city_url_list = response.css('.city_selection_section a::attr(href)').extract()
        for city in city_url_list:
            for price in ['p' + str(i) for i in range(1, 8)]:
                for area in ['a' + str(j) for j in range(1, 8)]:
                    for level in ['l' + str(m) for m in range(1, 7)]:
                        yield scrapy.Request(
                            url=city + 'ershoufang/' + price + area + level + '/',
                            callback=self.parse_city
                        )

    def parse_city(self, response):
        self.parse_page(response)
        max_p = response.css('.house-lst-page-box::attr(page-data)').extract_first()
        try:
            max_page = json.loads(max_p)['totalPage']
        except:
            logging.warning(max_p)
            raise CloseSpider('停止爬虫')
        if max_page != 1:
            for page in range(2, max_page + 1):
                yield scrapy.Request(
                    url=response.url[:-1] + 'pg' + str(page) + '/',
                    callback=self.parse_page
                )

    def parse_page(self, response):
        house_url_list = re.findall(r'https://.{2,5}\.lianjia\.com/ershoufang/\d*?\.html', response.text)
        if house_url_list == []:
            raise CloseSpider('找不到详情页的url')
        for house_url in house_url_list:
            yield scrapy.Request(
                url=house_url,
                callback=self.parse_detail
            )

    def parse_detail(self, response):
        item = LianjiaItem()
        house_show = response.css('.content ul:first-child li *::text').extract()
        house_detail = [i.strip() for i in house_show if i.strip() != '']
        item['house_room'] = house_detail[1]
        item['float_num'] = house_detail[3]
        item['house_area'] = house_detail[5]
        item['house_struct'] = house_detail[7]
        item['real_area'] = house_detail[9]
        item['house_type'] = house_detail[11]
        item['face_position'] = house_detail[13]
        item['house_material'] = house_detail[15]
        item['fit_up'] = house_detail[17] # fit up vi. 装修
        item['people_float_percent'] = house_detail[19]
        item['have_float'] = house_detail[21]
        item['owner_year'] = house_detail[23]
        item['sale_time'] = house_detail[25]
        item['sale_type'] = house_detail[27]
        item['last_sale'] = house_detail[29]
        item['house_useby'] = house_detail[31]
        item['house_age'] = house_detail[33]
        item['owner_is'] = house_detail[35]
        item['is_mortgage'] = house_detail[37] # mortgage vi. n. 抵押/抵押物
        item['have_passport'] = house_detail[39]
        item['total_price'] = response.css('.price .total::text').extract_first() + '万'
        item['average_price'] = response.css('.unitPriceValue::text').extract_first()
        item['product_time'] = response.css('.area .subInfo::text').extract_first()
        item['area_in'] = ' '.join(response.css('.areaName .info a::text').extract())
        item['community_name'] = response.css('a.info::text').extract_first()
        yield item
