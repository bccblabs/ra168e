import scrapy, re
from itertools import product
from ra168e.items import vehicle_urls
import os
from pymongo import MongoClient

mongo_host_name = os.environ['VEHICLE_DATA_PORT_27017_TCP_ADDR']
mongo_port = int(os.environ['VEHICLE_DATA_PORT_27017_TCP_PORT'])

client = MongoClient(mongo_host_name, mongo_port)

model_stats_db = client['cars']
model_stats_coll = model_stats_db.urls

uploaded_db = client['upload_set']
uploaded_coll = uploaded_db.uploaded

import pickle

global urls_list
urls_list = model_stats_coll.distinct ('listing_url')
global makes

makes = [u'aston--martin', u'audi', u'bentley', u'bmw', u'bugatti', u'cadillac', u'ferrari', u'infiniti', u'jaguar', u'lamborghini', u'land--rover', u'lexus', u'lotus', u'maserati', u'mclaren', u'mercedes-benz', u'porsche', u'rolls-royce'
]

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

class dupont_spider (scrapy.Spider):
	name='dupont'
	pf_path = '/urls/'
	makes = []

	def __init__(self, batch):
		self.makes = list (set(pickle.load (open (self.pf_path + batch + '.p', 'rb' ) ) ) )

	def start_requests(self):
		request_list=[]
		for make in self.makes:
			index_url = 'http://www.dupontregistry.com/autos/results/%s/all/all/refine?distance=0&inv=false&pagenum=1&perpage=100&sort=price_desc' %(make)
			request_list.append (scrapy.Request (index_url, callback=self.parse_first_page_listings))
		return request_list

	def parse_page_listings (self, response):
		listing_page_urls = ['http://www.dupontregistry.com/autos/' + x.replace ('../../../../', '') for x in response.xpath ('//a[contains(@class, "car_title")]/@href').extract()]
		for page_url in listing_page_urls:
			if page_url not in urls_list:
				yield scrapy.Request (page_url, callback=self.parse_page, dont_filter=True)

	def parse_first_page_listings (self, response):
		self.parse_page_listings (response)
		last_page_num = [int(x) for x in response.xpath ('//ul[@class="paging"]/li/a/text()').extract() if x.isdigit()][-1]
		for x in range (2, last_page_num + 1):
			page_idx_url = response.url.replace ('pagenum=1', 'pagenum=%d'%(x))
			yield scrapy.Request (page_idx_url, callback=self.parse_page_listings, dont_filter=True)


	def parse_page (self, response):
		item = vehicle_urls()
		item['listing_url'] = response.url
		item['image_urls'] = [ 'http://www.dupontregistry.com' + x for x in response.xpath ('//div[contains(@class="slideshow gallery-js-ready autorotation-disabled", @style="display: block; opacity: 0;")]/img/@src').extract() if '570' in x]
		keys = [x.strip().lower() for x in response.xpath ('//table[contains (@class, "simple-table modTable")]/tbody/tr/th/text()').extract()]
		values = [x.strip().lower() for x in response.xpath ('//table[contains (@class, "simple-table modTable")]/tbody/tr/td/text()').extract()]
		yr_mk_md = response.url.strip('http://www.dupontregistry.com/autos/listing/').split ('/')
		item['make'] = yr_mk_md[1].strip('').lower().replace ("--", " ").strip()
		item['model'] = yr_mk_md[2].strip('').lower().replace ("--", " ").strip()

		for x in zip (keys, values):
			if x[0] == 'year' and x[1].isdigit():
				item['year'] = int (x[1])
			if x[0] == 'body style':
				item['bodyType'] = x[1]
		return item

class ImagesSpider (scrapy.Spider):
	name="cars"
	special_makes = ['Mercedes-Benz', 'Rolls-Royce']
	two_word_makes = ['land rover', 'aston martin', 'alfa romeo', 'avanti motors']
	bad_photo_kwd = ['stock', 'search', 'car-pictures.cars.com']
	body_styles_kwd = ['convertible', 'coupe', 'hatchback', 'truck', 'suv', 'wagon', 'minivan', 'sedan', 'pickup', 'van']

	pf_path = '/ubuntu/home/ra168e/ra168e/urls/'
	index_urls = []

	def __init__ (self, batch):
		self.index_urls = list(set(pickle.load (open (self.pf_path + batch + '.p', 'rb') ) ) )

	def start_requests(self):
		request_list = []
		for index_url in self.index_urls:
			request_list.append(scrapy.Request (index_url, callback=self.parse_index_page, dont_filter=True))
		return request_list

	def parse_index_page (self, response):
		links = [listing_link for listing_link in response.xpath ('//a[contains(@class, "js-vr-vdp-link")]/@href').extract() if 'photo' not in listing_link]
		for x in links:
			if "http://www.cars.com" + x not in urls_list:
				yield scrapy.Request ('http://www.cars.com' + x, callback=self.parse_vehicle_info, dont_filter=True)

	def parse_vehicle_info(self, response):
		item = vehicle_urls()
		try:
			details_list = [ s.lower() for s in response.xpath ('//ul[contains(@class, "vehicle-details list")]/child::li/text()').extract()]
			item['keywords'] = details_list
			item['listing_url'] = response.url
			tmp_body_style_list = filter (lambda item: any(x for x in self.body_styles_kwd if x in item), details_list)
			if len(tmp_body_style_list) > 0:
				item['bodyType'] = tmp_body_style_list[0]
			else:
				item['bodyType'] = ''

			info_str = [ x.strip(',').lower() for x in filter (None, response.xpath('//title/text()').extract()[0].split(' ')) if x.strip(',').isalnum() or x in self.special_makes or '-' in x]
			item['year'] = info_str[0]
			item['listing_id'] = re.findall (r'\d+', response.url)[0]
			if info_str[1] == 'land' and info_str[2] == 'rover':
				item['make'] = 'land rover'
				item['model'] = ' '.join(info_str[3:]).replace('-', ' ').strip()
			elif info_str[1] == 'aston' and info_str[2] == 'martin':
				item['make'] = 'aston martin'
				item['model'] = ' '.join(info_str[3:]).replace('-', ' ').strip()
			elif info_str[1] == 'alfa' and info_str[2] == 'romeo':
				item['make'] = 'alfa romeo'
				item['model'] = ' '.join(info_str[3:]).replace('-', ' ').strip()
			elif info_str[1] == 'avanti' and info_str[2] == 'motors':
				item['make'] = 'avanti motors'
				item['model'] = ' '.join(info_str[3:]).replace('-', ' ').strip()
			else:
				item['make'] = info_str[1]
				item['model'] = ' '.join(info_str[2:]).replace('-', ' ').strip()


		except:
			scrapy.log.msg ("url (%s) scrapy error" %(response.url), level=ERROR)
		finally:
			img_req = scrapy.Request (response.url.replace('overview', 'photo'), callback=self.parse_vehicle_img_urls)
			img_req.meta['item'] = item
			return img_req

	def parse_vehicle_img_urls(self, response):
		item = response.meta['item']
		item['image_urls'] = filter (lambda url: not any ([x for x in self.bad_photo_kwd if x in url]), response.xpath('//img[contains(@class, "photo")]/@data-def-src').extract())
		return item

