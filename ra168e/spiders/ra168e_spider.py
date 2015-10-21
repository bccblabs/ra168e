import scrapy, re, os, json, pickle, logging, glob
from itertools import product, izip
from ra168e.items import issues, entry
from pymongo import MongoClient
from selenium import webdriver
from scrapy.exceptions import DropItem
#mongo_host_name = os.environ['VEHICLE_DATA_PORT_27017_TCP_ADDR']
#mongo_port = int(os.environ['VEHICLE_DATA_PORT_27017_TCP_PORT'])
mongo_host_name = 'localhost'
mongo_port = 27017

client = MongoClient(mongo_host_name, mongo_port)

vehicle_data_db = client['vehicle_data']
issues_collection = vehicle_data_db.issues_v3

issues_vehicles_list = issues_collection.distinct ('name')

odi_makes = [
"AM GENERAL",
"VOLVO",
"VOLKSWAGEN",
"TOYOTA",
"TESLA",
"SUZUKI",
"SUPER DUTY",
"SUBARU",
"SRT",
"SCION",
"SATURN",
"SAAB",
"ROLLS-ROYCE",
"RAM",
"PORSCHE",
"PONTIAC",
"NISSAN",
"MITSUBISHI",
"MINI",
"MERCURY",
"MERCEDES-BENZ",
"MERCEDES BENZ",
"MERCEDES",
"MCLAREN",
"MAZDA",
"MASERATI",
"LOTUS",
"LINCOLN",
"LEXUS",
"LAND ROVER",
"LAMBORGHINI",
"KOENIGSEGG",
"KIA",
"JEEP",
"JAGUAR",
"ISUZU",
"INFINITI",
"HYUNDAI",
"HONDA",
"GMC",
"FORD",
"FISKER",
"FIAT",
"FERRARI",
"DODGE",
"CHRYSLER",
"CHEVROLET",
"CADILLAC",
"BUICK",
"BUGATTI",
"BMW",
"BENTLEY",
"AUDI",
"ASTON MARTIN",
"ALFA"
"ACURA"]

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def construct_odi_url (year, make, model, model_id):
	url = "http://www-odi.nhtsa.dot.gov/owners/SearchResults?prodType=V&searchType=PROD&targetCategory=A&searchCriteria.model=%s&searchCriteria.model_yr=%s&searchCriteria.make=%s&searchCriteria.prod_ids=%s" %(model, year, make, model_id)
	return url

class odi (scrapy.Spider):
	name = "odi"
	json_path = '/Users/bski/Project/ra168e_odi/ra168e/ra168e/json/*.json'
	def __init__ (self):
		self.driver = webdriver.PhantomJS('phantomjs')		
		self.driver.set_page_load_timeout (30)

	def parse_stats(self, btn_selector_string, stats_selector_string, vehicle):
		items_list = []
		div_btn = self.driver.find_element_by_xpath (btn_selector_string)
		if div_btn.is_displayed():
			div_btn.click()
			div_text = [x.text for x in self.driver.find_elements_by_xpath (stats_selector_string)]
			for text in div_text:
				logging.info ( '[%s] scrapped component info %s' % (vehicle, text)) 
				if "All" not in text:
					stats_item = entry()	
					stats_item['component'] = text[0:text.find("(")].strip().lower().encode ('utf-8')
					stats_item['count'] = int (re.findall (r'\d+', text)[0])
					items_list.append (stats_item)
		return items_list

	def start_requests(self):
		data = {}
		for x in glob.glob (self.json_path):
			with open (x) as f:
				data = json.load (f)
				for item in data.items():
					for years in item[1]:
						year = years['Y']
						for makes in years['makes']:
							if makes['m'] in odi_makes:
								make = makes['m']
								for model in makes['models']:
									issue_item = issues()
									model_name = model['o']
									mid_string = model['s']
									mid, recalls, investigations, complaints, tsbs = mid_string.split (",") 
									issue_item['name'] = "%s %s %s" %(year, make, model_name)
									issue_item['count'] = int (complaints)
									if issue_item['name'] not in issues_vehicles_list:
										request = scrapy.Request (construct_odi_url (year, make, model_name, mid), callback=self.parse_page)
										request.meta['issue_item'] = issue_item
										yield request

	def parse_page (self, response):
		issue_item = response.meta['issue_item']
		self.driver.get (response.url)
		issue_item['details'] = []
		for x in self.parse_stats ('//a[@id="complaints-tab"]', '//select[@id="component_det_cmpl"]/option', issue_item['name']):
			issue_item['details'].append (x)
		if len (issue_item['details']) == 0 and issue_item['count'] > 0:
			msg = "vehicle stats [%s] has %d length stats, %d expected... [%s]" %(issue_item['name'], len(issue_item['details']), issue_item['count'], response.url)
			logging.warning (msg)
			raise DropItem (msg)
		return issue_item