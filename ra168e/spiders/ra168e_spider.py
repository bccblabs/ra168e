import scrapy, re, os, json, pickle
from itertools import product, izip
from ra168e.items import vehicle_urls, zero_sixty, issues, entry, safety, safety_entry
from pymongo import MongoClient
from selenium import webdriver

# mongo_host_name = os.environ['VEHICLE_DATA_PORT_27017_TCP_ADDR']
# mongo_port = int(os.environ['VEHICLE_DATA_PORT_27017_TCP_PORT'])
mongo_host_name = 'localhost'
mongo_port = 27017

client = MongoClient(mongo_host_name, mongo_port)

model_stats_db = client['cars']
model_stats_coll = model_stats_db.urls

uploaded_db = client['upload_set']
uploaded_coll = uploaded_db.uploaded

vehicle_data_db = client['vehicle_data']
issues_collection = vehicle_data_db.issues

issues_vehicles_list = issues_collection.distinct ('name')

global makes
global urls_list
urls_list = model_stats_coll.distinct ('listing_url')

makes = [
u'aston--martin',
u'audi',
u'bentley',
u'bmw',
u'bugatti',
u'cadillac',
u'ferrari',
u'infiniti',
u'jaguar',
u'lamborghini',
u'land--rover',
u'lexus',
u'lotus',
u'maserati',
u'mclaren',
u'mercedes-benz',
u'porsche',
u'rolls-royce'
]

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def construct_odi_url (year, make, model, model_id):
	url = "http://www-odi.nhtsa.dot.gov/owners/SearchResults?prodType=V&searchType=PROD&targetCategory=A&searchCriteria.model=%s&searchCriteria.model_yr=%s&searchCriteria.make=%s&searchCriteria.prod_ids=%s" %(model, year, make, model_id)
	return url


class iihs (scrapy.Spider):
	name='iihs'
	json_path = '/Users/bski/Project/image_training/ra168e/ra168e/json/iihs/'
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

class odi (scrapy.Spider):
	name = "odi"
	json_path = '/Users/bski/Project/image_training/ra168e/ra168e/json/'
	def __init__ (self, file_name):
		self.json_file_name = file_name
		self.driver = webdriver.PhantomJS()		

	def parse_stats(self, btn_selector_string, stats_selector_string):
		items_list = []
		try:
			div_btn = self.driver.find_element_by_xpath (btn_selector_string)
			div_btn.click()
			div_text = [x.text for x in self.driver.find_elements_by_xpath (stats_selector_string)]
			for text in div_text:
				if "All" not in text:
					try:
						stats_item = entry()	
						stats_item['component'] = text[0:text.find("(")].strip().lower()
						stats_item['count'] = int (re.findall (r'\d+', text)[0])
						items_list.append (stats_item)
					except:
						pass
		except:
			pass
		return items_list

	def start_requests(self):
		request_list = []
		data = {}
		with open (self.json_path + self.json_file_name) as f:
			data = json.load (f)
		for item in data.items():
			for years in item[1]:
				year = years['Y']
				for makes in years['makes']:
					make = makes['m']
					for model in makes['models']:
						issue_item = issues()
						model_name = model['o']
						mid_string = model['s']
						mid, recalls, investigations, complaints, tsbs = mid_string.split (",") 
						issue_item['name'] = "%s %s %s" %(year, make, model_name)
						issue_item['recalls_cnt'] = int (recalls)
						issue_item['investigations_cnt'] = int (investigations)
						issue_item['complaints_cnt'] = int (complaints)
						issue_item['tsbs_cnt'] = int (tsbs)
						if issue_item['name'] not in issues_vehicles_list:
							request = scrapy.Request (construct_odi_url (year, make, model_name, mid), callback=self.parse_page)
							request.meta['issue_item'] = issue_item
							request_list.append (request)
		return request_list

	def parse_page (self, response):
		issue_item = response.meta['issue_item']
		try:
			self.driver.get (response.url)
			issue_item['recall_stats'] = self.parse_stats ('//a[@id="recalls-tab"]', '//select[@id="component_det_rcl"]/option')
			issue_item['investigation_stats'] = self.parse_stats ('//a[@id="investigations-tab"]', '//select[@id="component_det_inv"]/option')
			issue_item['complain_stats'] = self.parse_stats ('//a[@id="complaints-tab"]', '//select[@id="component_det_cmpl"]/option')
		except:
			pass
		return issue_item

class zs (scrapy.Spider):
	name='zs'
	makes_urls = []
	def __init__(self, makes_p):
		self.makes_urls = list(set(pickle.load (open (makes_p, 'rb'))))

	def start_requests(self):
		request_list = []
		for x in self.makes_urls:
			request_list.append (scrapy.Request (x, callback=self.parse_zs))
		return request_list

	def parse_zs(self, response):
		times = [x.strip() for x in response.xpath('//div[contains(@class, "accordion opened")]/div/div/span[contains(@class, "statTimes")]/text()').extract()]		
		zs = [float (str(x.replace ("0-60 mph ", "").replace("0-60 To Be Released", "-1.0"))) for x in times if "0-60" in x]
		titles = [x.strip().replace('(', '').replace(')', '') for x in response.xpath('//span[contains(@class, "statTitle")]/text()').extract()]
		for x in izip (titles, zs):		
			scrapped_item = zero_sixty()
			scrapped_item['name'] = x[0].lower()
			scrapped_item['zs'] = x[1]
			yield scrapped_item

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

	pf_path = '/urls/'
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

