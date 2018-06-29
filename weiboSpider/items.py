# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeibospiderItem(scrapy.Item):
    # define the fields for your item here like:
    username=scrapy.Field()#用户名字
    fenshinum=scrapy.Field()#粉丝数量

    allweibonum=scrapy.Field()#用户发布微博数量
    uid=scrapy.Field()#用户ID
    weibocontent=scrapy.Field()#内容
    pinglun=scrapy.Field()#评论数
    zhuanfa=scrapy.Field()#转发数
    fabushijian=scrapy.Field()#发布时间
    diqu=scrapy.Field()#所在地区
    dianzhan=scrapy.Field()#点赞数
    gender=scrapy.Field()#性别
    renzheng=scrapy.Field()#认证
    birthday=scrapy.Field()#生日
    jianjie=scrapy.Field()#简介
    biaoqian=scrapy.Field()#标签
    education=scrapy.Field()#教育信息

class FanItem(scrapy.Item):
    username = scrapy.Field()  # 用户名字
    fenshinum = scrapy.Field()  # 粉丝数量
    allweibonum = scrapy.Field()  # 用户发布微博数量
    uid = scrapy.Field()  # 用户ID
    content = scrapy.Field()  # 内容
    pinglun = scrapy.Field()  # 评论数
    zhuanfa = scrapy.Field()  # 转发数
    fabushijian = scrapy.Field()  # 发布时间
    diqu = scrapy.Field()  # 所在地区
    dianzhan = scrapy.Field()  # 点赞数
    gender = scrapy.Field()  # 性别
    renzheng = scrapy.Field()  # 认证
    birthday = scrapy.Field()  # 生日
    jianjie = scrapy.Field()  # 简介
    biaoqian = scrapy.Field()  # 标签
    education = scrapy.Field()  # 教育信息