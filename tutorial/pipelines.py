# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
import MySQLdb
import hashlib
from scrapy.exceptions import DropItem
from scrapy.http import Request
from scrapy import signals
from scrapy.exceptions import DropItem

class DuplicatesPipeline(object):
	def __init__(self):
		self.ids_seen = set()

	def process_item(self, item, spider):
		if item['productDel'] in self.ids_seen:
			raise DropItem("Duplicate item found: %s" % item)
		else:
			self.ids_seen.add(item['productDel'])
			return item

class PricePipeline(object):
	
	def process_item(self, item, spider):
		if item['price']:
			return item
		else:
			raise DropItem("Missing price in %s" % item)

class MysqlPipeline(object):
	
	def __init__(self):
		self.conn = MySQLdb.connect(user='root', passwd='******', db='muying', host='localhost', charset="utf8", use_unicode=True)
		self.cursor = self.conn.cursor()

	def process_item(self, item, spider):
		try:
			self.cursor.execute("""INSERT INTO muying_product (bigCate, smallCate, productDetail,
			brand, price) VALUES (%s, %s, %s, %s, %s)""", (item['BigCate'].encode('utf-8'),
				item['aSmallCate'].encode('utf-8'),
				item['productDel'].encode('utf-8'), item['brand'].encode('utf-8'),
				item['price'].encode('utf-8')))
			self.conn.commit()
		except MySQLdb.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])
		return item

