# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.exceptions import DropItem
import csv
class WeibospiderPipeline(object):
    def __init__(self):
        self.file=open('weibo.json','w')
        self.info={}
    def process_item(self, item, spider):
        uid=item['uid']
        self.info[uid]=dict(item)
        # line=json.dumps(dict(item),ensure_ascii=False)+"\n"
        # self.file.write(line)
        return item
    def close_spider(self,spider):
        json.dump(self.info,fp=self.file,indent=4,ensure_ascii=False)
        self.file.close()

