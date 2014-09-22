# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class LawItem(scrapy.Item):
    name = scrapy.Field()

class DeputyItem(scrapy.Item):
    name = scrapy.Field()
    party = scrapy.Field()
    state = scrapy.Field()
    active = scrapy.Field()
    deputy_id = scrapy.Field()
    #deputy_register = scrapy.Field()
