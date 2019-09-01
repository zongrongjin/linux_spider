# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ErshoufangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class LianjiaItem(scrapy.Item):
    house_room = scrapy.Field()
    float_num = scrapy.Field()
    house_area = scrapy.Field()
    house_struct = scrapy.Field()
    real_area = scrapy.Field()
    house_type = scrapy.Field()
    face_position = scrapy.Field()
    house_material = scrapy.Field()
    fit_up = scrapy.Field() #装修
    people_float_percent = scrapy.Field()
    have_float = scrapy.Field()
    owner_year = scrapy.Field()
    sale_time = scrapy.Field()
    sale_type = scrapy.Field()
    last_sale = scrapy.Field()
    house_useby = scrapy.Field()
    house_age = scrapy.Field()
    owner_is = scrapy.Field()
    is_mortgage = scrapy.Field() #mortgage 抵押
    have_passport = scrapy.Field()
    total_price = scrapy.Field()
    average_price = scrapy.Field()
    product_time = scrapy.Field()
    area_in = scrapy.Field()
    community_name = scrapy.Field()