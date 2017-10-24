# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
# "scrapy_url":"抓取的URL"
# "cname":"◎译　　名",
# "ename":"◎片　　名",
# "year":"◎年　　代",
# "address":"◎产　　地",
# "catogray":"◎类　　别",
# "lan":"◎语　　言",
# "subtitle":"◎字　　幕",
# "showdate":"◎上映日期",
# "db_score":"◎豆瓣评分",
# "IMDb_score":"◎IMDb评分",
# "file_type":"◎文件格式",
# "movie_size":"◎视频尺寸",
# "file_size":"◎文件大小",
# "movie_mins":"◎片　　长",
# "director":"◎导　　演",
# "starring":"◎主　　演",
# "desc":"◎简　　介",
# "clipimgs":"◎影片截图"
# "publishdate":"发布日期"
class ScrapylessItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    poster = scrapy.Field();
    cname = scrapy.Field();
    ename = scrapy.Field();
    year = scrapy.Field();
    address = scrapy.Field();
    catogray = scrapy.Field();
    lan = scrapy.Field();
    subtitle = scrapy.Field();
    showdate = scrapy.Field();
    db_score = scrapy.Field();
    IMDb_score = scrapy.Field();
    file_type = scrapy.Field();
    movie_size = scrapy.Field();
    file_size = scrapy.Field();
    movie_mins = scrapy.Field();
    director = scrapy.Field();
    starring = scrapy.Field();
    desc = scrapy.Field();
    clipimgs = scrapy.Field();
    downloadurl = scrapy.Field();
    publishdate = scrapy.Field();
    scrapy_url = scrapy.Field();
    tmp_scrapy_url = scrapy.Field();
    pass
