import scrapy, re, os, json, pickle
from itertools import product, izip
from ra168e.items import vehicle_urls, zero_sixty, issues, entry, safety, safety_entry
from pymongo import MongoClient

mongo_host_name = os.environ['VEHICLE_DATA_PORT_27017_TCP_ADDR']
mongo_port = int(os.environ['VEHICLE_DATA_PORT_27017_TCP_PORT'])

client = MongoClient(mongo_host_name, mongo_port)

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

class iihs (scrapy.Spider):
	name='iihs'
	json_path = '/ra168e/ra168e/json/iihs/'
	base_url = 'http://www.iihs.org'

	def parse_entries(self, response, key_xpath, value_xpath):
		kv_list = []
		try:
			keys = list(set(response.xpath (key_xpath).extract()))
			values = list(set(response.xpath (value_xpath).extract()))
			for kv in zip (keys, values):
				entry = safety_entry()
				entry['name'] = kv[0]
				entry['value'] = kv[1]
				kv_list.append (entry)
		except:
			pass

		return kv_list

	def start_requests(self):
		request_list = []
		src_list = list(set(pickle.load (open(self.json_path + 'iihs_urls.p'))))
		for url in src_list:
			request_list.append (scrapy.Request (self.base_url + url, callback=self.parse_year_urls, dont_filter=True))
		return request_list

	def parse_year_urls(self, response):
		links_by_year = response.xpath('//div[contains(@class, "dropdown year-dropdown")]/ul/li/a/@href').extract()
		for x in links_by_year:
			yield scrapy.Request (self.base_url + x, callback=self.parse_page, dont_filter=True)

	def parse_page (self, response):
		safety_doc = safety()
		try:
			safety_doc['name'] = response.xpath ('//h1[contains(@class, "main-caption")]/text()').extract()[0]

			safety_doc['ratings'] = self.parse_entries (response,
														'//ul[contains(@class, "rating-list")]/li/div[contains(@class, "rating-caption")]/text()',
														'//ul[contains(@class, "rating-list")]/li/div[contains(@class, "rating-icon")]/div/span/@title')
			safety_doc['videos'] = self.parse_entries (	response,
														'//a[contains(@class, "play-vid")]/text()',
														'//a[contains(@class, "play-vid")]/@data-videoid')
			safety_doc['photos'] = self.parse_entries (	response,
														'//a[contains(@class, "vehicle-image-thumbnail")]/div/strong/text()',
														'//a[contains(@class, "vehicle-image-thumbnail")]/img/@src')
			safety_doc['equipments'] = response.xpath ('//div[contains(@class, "feature-value")]/text()').extract()
		except:
			pass
		return safety_doc


