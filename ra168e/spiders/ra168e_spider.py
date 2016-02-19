
from itertools import product
from pymongo import MongoClient
from ra168e.items import listing_item, vehicle_urls, zipcity
import scrapy, json, pickle
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

class edmunds_spider (scrapy.Spider):
	name="edmunds_listings"
	edmunds_root_url = "https://api.edmunds.com/"
	edmunds_listings_endpoint="https://api.edmunds.com/api/inventory/v2/styles/"
	key="d442cka8a6mvgfnjcdt5fbns",
	secret="tVsB2tChr7wXqk47ZZMQneKq"
	auth_endpoint = "https://api.edmunds.com/inventory/token"
	next_expiration = -1	
	access_token = ""
	all_urls = []
	handle_httpstatus_list = [401, 403]
	failed_urls = []
	processed_urls_cnt = 0
	def __init__ (self):
		dispatcher.connect(self.handle_spider_closed, signals.spider_closed) 
		mongo_host_name = 'localhost'
		mongo_port = 27017
		client = MongoClient(mongo_host_name, mongo_port)

		zipcode_coll = client['zipcodes'].cities
		styleids_coll = client['vehicle_data'].styleIds

		styleidList = styleids_coll.distinct ('styleId')

		for x in zipcode_coll.find ({'city': {"$regex": "FL"}}):
			for y in styleidList:
				listing_url = self.edmunds_listings_endpoint + str(y)
				formated_url = "{0}?zipcode={1}&radius=25&pagenum=1&pagesize=50&view=full&fmt=json".format (listing_url, x['zipcode'])
				self.all_urls.append (formated_url)



	def start_requests (self):
		yield scrapy.FormRequest (
								url=self.auth_endpoint, 
								headers={
									"Content-Type": "application/x-www-form-urlencoded"
								},
								formdata={
										"client_id": self.key,
										"client_secret": self.secret,
										"grant_type": "client_credentials"
								},
								callback=self.start_listings_requests,
								dont_filter=True)

	def start_listings_requests (self, response):
		resp = json.loads (response.body)
		self.next_expiration = resp['expires_in']
		self.access_token = resp['access_token']
		self.logger.info ('[access token parsed]')
		self.logger.info ('[start listings requests]')
		for url in self.all_urls:
			yield scrapy.Request (
				url, 
				headers={
					"Authorization": "Bearer " + self.access_token
				},
				callback=self.parse_listing, 
				dont_filter=True)


	def retry_parse_listings (self, response):
		if response.status >= 400:
			self.logger.info ('[Bad Repsonse Code] again,,, saving to retry urls <{0}>'.format (response.status))
			self.crawler.stats.inc_value('failed_url_count')
			self.failed_urls.append(response.url)
		else:
			request_url = response.request.meta['retry_url']
			self.logger.info ('[Recover Bad Url] <{0}> '.format (request_url))
			resp = json.loads (response.body)
			self.next_expiration = resp['expires_in']
			self.access_token = resp['access_token']
			self.logger.info ('[access token parsed]')
			self.logger.info ('[retry listings requests]')

			yield scrapy.Request (
				request_url, 
				headers={
					"Authorization": "Bearer " + self.access_token
				},
				callback=self.parse_listing, 
				dont_filter=True)


	def parse_listing (self, response):
		if response.status == 401 or response.status == 403:
			self.logger.info ('[Bad Repsonse Code] <{0}> parsing page'.format (response.status))
			yield scrapy.FormRequest (
									url=self.auth_endpoint, 
									headers={
										"Content-Type": "application/x-www-form-urlencoded"
									},
									meta={
										'retry_url': response.url
									},
									formdata={
											"client_id": self.key,
											"client_secret": self.secret,
											"grant_type": "client_credentials"
									},
									callback=self.retry_parse_listings,
									dont_filter=True)
		else:
			self.logger.info ('<{0}> parsing page'.format (response.status))
			styleId = ""
			resp = json.loads (response.body)
			for listing in resp['inventories']:
				edmunds_listing = listing_item()
				if 'colors' in listing:
					edmunds_listing['colors'] = [{'name': x['name'], 'desc': x['category']} for x in listing['colors']]
				if 'mileage' in listing:
					edmunds_listing['mileage'] = listing['mileage']
				if 'small' in listing['media']['photos']:
					edmunds_listing['photos'] = listing['media']['photos']['small']['links']
				if 'listedSince' in listing:
					edmunds_listing['listedSince'] = listing['listedSince']
				if 'stockNumber' in listing:
					edmunds_listing['stockNumber'] = listing['stockNumber']
	
				edmunds_listing['dealer'] = listing['dealer']
				edmunds_listing['make'] = listing['make']['niceName']
				edmunds_listing['model'] = listing['model']['niceName']
				if 'options' in listing:
					try:
						edmunds_listing['options'] = [{'name': x['name'], 'desc': x['description']} for x in listing['equipment'] if x['equipmentType'] == 'OPTION']
					except:
						edmunds_listing['options'] = [{'name': x['name']} for x in listing['equipment'] if x['equipmentType'] == 'OPTION']

				edmunds_listing['prices'] = listing['prices']
				edmunds_listing['styleId'] = listing['style']['id']
				edmunds_listing['trim'] = listing['style']['trim']
				edmunds_listing['vin'] = listing['vin']
				edmunds_listing['year'] = listing['year']['year']
				styleId = edmunds_listing['styleId']
				yield edmunds_listing

			next = [x for x in resp['links'] if x['rel'] == 'next']
			if next != None and len(next) > 0 and next[0]['href'] != response.url:
				self.logger.info ('[yielding pages request] ' + next[0]['href'])
				yield scrapy.Request (
					self.edmunds_root_url + next[0]['href'], 
					headers={
						"Authorization": "Bearer " + self.access_token
					},
					callback=self.parse_listing, 
					dont_filter=True)
			else:
				self.processed_urls_cnt = self.processed_urls_cnt + 1
				self.logger.info ('[{0} done with {1}/{2} total requests ]'.format (styleId, self.processed_urls_cnt, len (self.all_urls)))

	def handle_spider_closed(self, spider, reason): # added self 
		self.crawler.stats.set_value('failed_urls',','.join(spider.failed_urls))
		with open('retry_urls.txt', 'w') as outfile:
		    json.dump(spider.failed_urls, outfile)
	def process_exception(self, response, exception, spider):
		ex_class = "%s.%s" % (exception.__class__.__module__,  exception.__class__.__name__)
		self.crawler.stats.inc_value('downloader/exception_count', spider=spider)
		self.crawler.stats.inc_value('downloader/exception_type_count/%s' % ex_class, spider=spider)
