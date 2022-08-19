# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaparserItem(scrapy.Item):
    user_id = scrapy.Field()
    username = scrapy.Field()
    # photo = scrapy.Field()
    # likes = scrapy.Field()
    # post_data = scrapy.Field()
    friend_username = scrapy.Field()
    friend_fullname = scrapy.Field()
    friend_pic = scrapy.Field()
    follow_username = scrapy.Field()
    follow_fullname = scrapy.Field()
    follow_pic = scrapy.Field()
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
