# -*- coding: utf-8 -*-
import scrapy


class AnjukeSpider(scrapy.Spider):
    name = 'anjuke'
    allowed_domains = ['anjuke.com']
    start_urls = ['https://www.anjuke.com/sy-city.html']

    def parse(self, response):
        city_list = response.css('.city_list a::attr(href)').extract()
        for city in city_list:
            city_url = city + '/sale/'