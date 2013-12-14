from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item
from tutorial.items import DmozItem
import re


class DmozSpider(CrawlSpider):
	name = "dmoz"
	allowed_domains = ["muyingzhijia.com"]
	start_urls = [
			"http://www.muyingzhijia.com/Shopping/alllist.aspx",
			]
	rules = [
			Rule(SgmlLinkExtractor(allow=('/Shopping/category\.aspx\?cateID[\S]+', )), follow=True),
			Rule(SgmlLinkExtractor(allow=('/Shopping/subcategory\.aspx\?cateID[\S]+', )), follow=True),
			Rule(SgmlLinkExtractor(allow=('/shopping/ProductDetail\.aspx\?PdtId[\S]+', )), follow=True, callback='parse_product'),
			]
	
	def parse_product(self, response):
		sel = HtmlXPathSelector(response)
		item = DmozItem()
		str = sel.xpath('//a[@id="aBigCate"]/text()').extract()
		if str:
			res = re.search("[\S]+", str[0])
			item['BigCate'] = res.group()
#			item['BigCate'] = item['BigCate'].encode('utf-8')
		else:
			item['BigCate'] = ""
		str = sel.xpath('//a[@id="aSmallCate"]/text()').extract()
		if str:
			res = re.search("[\S]+", str[0])
			item['aSmallCate'] = res.group()
#			item['aSmallCate'] = (item['aSmallCate']).encode("utf-8")
		else:
			item['aSmallCate'] = ""
		str = sel.xpath('//div[@class="productDe001s"]/text()').extract()
		if str:
			res = re.search("[\S]+", str[0])
			item['productDel'] = res.group()
#			item['productDel'] = item['productDel'].encode("utf-8")
		else:
			item['productDel'] = ""
		str = sel.xpath('//span[@class="f_price f16 f_bold"]/strong/text()').extract()
		if str:
			res = re.search("[\S]+", str[0])
			item['price'] = res.group()
#			item['price'] = item['price'].encode("utf-8")
		else:
			item['price'] = ""
		str = sel.xpath('//div[@id="divseletedSC"]/text()').extract()
		if str:
			tag = 0
			for subStr in str:
				res = re.search("[\S]+", subStr)
				if res:
					item['brand'] = res.group()
			#		item['brand'] = item['brand'].encode("utf-8")
					tag = 1
					break
			if tag == 0:
				item['brand'] = ""
		else:
			item['brand'] = ""
		return item
