# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PeilvItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    cc  = scrapy.Field()#changci
    odd = scrapy.Field()#oddset
    li =  scrapy.Field()#libo
    b5  = scrapy.Field()#bet365
    inte  = scrapy.Field()#interwetten
    wl  = scrapy.Field()#weilian
    w  = scrapy.Field()#weide
    ao = scrapy.Field()  # aomen
    b10  = scrapy.Field()#10bet
    res = scrapy.Field()#result
    bstype = scrapy.Field()#bisaitype
