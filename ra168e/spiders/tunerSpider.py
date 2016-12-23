import pickle, re, scrapy
from scrapy.selector import Selector
from ra168e.items import tuningItem, listingItem, projectItem
from decimal import Decimal
from itertools import izip
from selenium import webdriver
from StringIO import StringIO
import json
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



	# address = '865 Jarvis Drive'
	# city = 'Morgan Hill'
	# dealerstate = 'CA'
	# phone = '+1(800)341-5480'
	# zipcode = '95037'

class DinanSpider (scrapy.Spider):
	name='dinan'
	rootUrl = 'http://www.dinancars.com/products/?series=1-Series&model=135is-e82&mid=1159'
	start_urls= [rootUrl]
	driver = webdriver.Firefox()
	wait = WebDriverWait (driver, 10)

	descriptionSelector = '//div[contains(@class, "product_description")]/p/text()'
	titleSelector = '//h1[contains(@class, "dinan_page_title")]/text()'
	skuSelector = '//div[contains (@class, "product_title")]/text()'
	itemTitleSelector = '//div[contains (@class, "product_desc_para")]//table//th//text()'
	itemContentSelector = '//div[contains (@class, "product_desc_para")]//table//td//text()'
	makeModelSelector = '//ul[contains(@class, "squared")]//li/text()'
	mediaSelector = '//div[contains(@class, "product_left")]//a/@href'
	priceSelector = '//div[contains(@class, "price_number")]//text()'
	detailsSelector = '//div[contains (@class, "desc_info_cont info_cont")]//text()'
	def parse (self, resp):
		self.driver.get (resp.url)
		self.logger.info ('product index %s', resp.url)
		try:
			paginate = self.driver.find_element_by_class_name ("paginateResults")
			paginationOpts = paginate.find_elements_by_tag_name ('option')
			for x in paginationOpts:
				x.click()
				page = self.wait.until (EC.presence_of_element_located((By.CLASS_NAME, "product-cont")))
				product_urls = [x.get_attribute ('href') for x in page.find_elements_by_xpath('//div[@class="name"]/a')]
				for link in product_urls:
					yield scrapy.Request (link, self.parseProductDetails)
		except:
			page = self.wait.until (EC.presence_of_element_located((By.CLASS_NAME, "product-cont")))
			product_urls = [x.get_attribute ('href') for x in page.find_elements_by_xpath('//div[@class="name"]/a')]
			for link in product_urls:
				yield scrapy.Request (link, self.parseProductDetails)

	def parseProductDetails (self, resp):
		self.logger.info ('product details %s', resp.url)
		items = parseAlnum (resp.xpath (self.itemContentSelector).extract())
		itemsTitle = parseAlnum (resp.xpath (self.itemTitleSelector).extract())
		scrapItem = tuningItem()
		scrapItem['name'] = cleanseField (resp.xpath (self.titleSelector).extract_first())
		scrapItem['sku'] = cleanseField (resp.xpath (self.skuSelector).extract_first())
		scrapItem['details'] = cleanseField (resp.xpath (self.detailsSelector))
		scrapItem['specs'] = [x + ': ' + y for x in itemsTitle for y in items]
		scrapItem['description'] = parseAlnum (resp.xpath (self.descriptionSelector).extract())
		scrapItem['media'] = [x for x in resp.xpath (self.mediaSelector).extract()]
		scrapItem['url'] = resp.url
		scrapItem['price'] = parseFloat (resp.xpath (self.priceSelector).extract_first())
		# for model in resp.xpath (self.makeModelSelector).extract():
		# 	scrapItem['makeModelString'] = cleanseField (model)
		# 	scrapItem['dealerName'] = 'Dinan'
		# 	scrapItem['dealerPhone'] = self.phone
		# 	scrapItem['dealerLogo'] = 'http://www.dinancars.com/wp-content/uploads/2016/04/logo.png'
		# 	scrapItem['dealerAddress'] = self.address
		# 	scrapItem['dealerCity'] = self.city
		# 	scrapItem['dealerState'] = self.dealerstate
		# 	scrapItem['dealerZip'] = self.zipcode
		yield scrapItem

# class HKSSpider (scrapy.Spider):
# 	name='hks'
# 	rootUrl = 'http://www.hksusa.com'
# 	start_urls = ['http://www.hksusa.com/makes/']

# 	makeNameSelector = '//a[contains (@class, "catgridname")]/text()'
# 	makesIndexLinks = '//a[contains (@class, "catgridname")]/@href'

# 	modelNameSelector = '//div[contains (@class, "SubCategoryList")]//li/a/text()'
# 	modelsIndexLinks = '//div[contains (@class, "SubCategoryList")]//li/a/@href'

# 	generationIndexLinks = modelsIndexLinks

# 	tuningCategoryIndexLinks = '//div[contains (@class, "SubCategoryListGrid")]//li//a/@href'
# 	productDetail = '//div[contains (@class, "ProductDetails")]//a/@href'
# 	productsSelector = '//div[contains (@class , "ProductDetails")]//a/@href'
# 	breadCrumbsSelector = '//div[contains (@id, "ProductBreadcrumb")]//li//text()'
# 	priceSelector = '//span[contains(@class, "ProductPrice")]/text()'
# 	skuSelector = '//span[contains (@class, "VariationProductSKU")]/text()'
# 	itemsSelector = '//div[contains (@class, "ProductDescriptionContainer")]//ul/li/text()'
# 	descriptionSelector = '//div[contains (@class, "ProductDescriptionContainer")]/p/text()'
# 	mediaSelector = '//div[contains (@class, "ProductTinyImageList")]//li//td/a/@rel'


# 	dealerName = 'HKS'
# 	dealerPhone = '855-800-7150'
# 	dealerLogo = 'http://cdn1.bigcommerce.com/n-dvzvde/7knkm4/product_images/hksusa_herobanner_250x85_min_1454441491__05343.jpg'
# 	def parse (self, resp):
# 		makes = [cleanseField (make) for make in resp.xpath (self.makeNameSelector).extract()]
# 		for make, link in izip (makes, resp.xpath (self.makesIndexLinks).extract()):
# 			self.logger.info ('parsing makes %s', link)
# 			req = scrapy.Request (link, self.parseModels)
# 			req.meta['makeModelString'] = make
# 			yield (req)

# 	def parseModels (self, resp):
# 		models = [cleanseField (model) for model in resp.xpath (self.modelNameSelector).extract()]
# 		for model, link in izip (models, resp.xpath (self.modelsIndexLinks).extract()):
# 			self.logger.info ('parsing models %s', link)
# 			req = scrapy.Request (link, self.parseGenerations)
# 			modelName = model
# 			req.meta['makeModelString'] = resp.request.meta['makeModelString'] + " " + modelName
# 			yield (req)

# 	def parseGenerations (self, resp):
# 		gens = [cleanseField (gen) for gen in resp.xpath (self.modelNameSelector).extract()]
# 		for gen, link in izip (gens, resp.xpath (self.generationIndexLinks).extract()):
# 			self.logger.info ('parsing gens %s', link)
# 			req = scrapy.Request (link, self.parseProductCategories)
# 			genName = gen
# 			req.meta['makeModelString'] = resp.request.meta['makeModelString'] + " " + genName
# 			yield (req)

# 	def parseProductCategories (self, resp):
# 		for link in resp.xpath (self.tuningCategoryIndexLinks).extract():
# 			self.logger.info ('parsing categories %s', link)
# 			req = scrapy.Request (link, self.parseProducts)
# 			req.meta['makeModelString'] = resp.request.meta['makeModelString']
# 			yield req

# 	def parseProducts (self, resp):
# 		for link in resp.xpath (self.productsSelector).extract():
# 			self.logger.info ('parsing products %s', link)
# 			req = scrapy.Request (link, self.parseProductDetails)
# 			req.meta['makeModelString'] = resp.request.meta['makeModelString']
# 			yield req

# 	def parseProductDetails (self, resp):
# 		scrapItem = tuningItem()
# 		breadCrumbs = [cleanseField (x) for x in resp.xpath (self.breadCrumbsSelector).extract()]
# 		scrapItem['title'] = breadCrumbs[-1]
# 		scrapItem['makeModelString'] = resp.request.meta['makeModelString']
# 		scrapItem['url'] = resp.url
# 		scrapItem['price'] = parseFloat (resp.xpath (self.priceSelector).extract_first())
# 		scrapItem['sku'] = cleanseField (resp.xpath (self.skuSelector).extract_first())
# 		scrapItem['media'] = list()
# 		scrapItem['items'] =  [cleanseField (x) for x in resp.xpath (self.itemsSelector).extract()]
# 		scrapItem['description'] = cleanseField (resp.xpath (self.descriptionSelector).extract_first())
# 		imagesJSONRaw = resp.xpath (self.mediaSelector).extract()
# 		for imageJSON in imagesJSONRaw:
# 			jsonIO = StringIO (imageJSON)
# 			scrapItem['media'].append (json.load (jsonIO).get ('largeimage'))
# 		scrapItem['dealerName'] = self.dealerName
# 		scrapItem['dealerPhone'] = self.dealerPhone
# 		scrapItem['dealerLogo'] = self.dealerLogo
# 		self.logger.info ('product details %s', resp.url)
# 		self.logger.info ('make model string: %s', scrapItem['makeModelString'])
# 		yield (scrapItem)
#


class RenntechSpider (scrapy.Spider):
	name="renntech"
	destType="" # car|project|manufacturer|package|part|
	rootUrl = 'http://www.renntechmercedes.com'
	blacklist = ['wheels', 'accessories', 'akrapovic', 'powersports']
	disallowedFields = ['back to', 'ecu', 'exhaust', 'air', 'drive', 'suspension', 'exhaust', 'renntech', 'products']
	def start_requests (self):
		indexUrl = self.rootUrl + '/index.php/products'
		return [scrapy.Request (indexUrl, callback=self.parseIndexPage)]

	def parseIndexPage (self, resp):
		productsByModel = resp.xpath ('//ul[contains(@id, "swmenu138-sub")]//a/@href').extract()
		for x in productsByModel:
			if (all(term not in x for term in self.blacklist)):
				print x
				yield scrapy.Request (self.rootUrl + x, callback=self.parseProducts, dont_filter=True)

	def parseModelIndexPage (self, resp):
		trimsByGen = resp.xpath ('//div[contains(@class, "category-view")]/div/div/h2/a/@href').extract()
		productsByGen = resp.xpath ('//div[contains(@class, "row")]/div/div/div/a/@href').extract()

		for x in trimsByGen:
			yield scrapy.Request (self.rootUrl + x, self.parseGenerations, dont_filter=True)
		for x in productsByGen:
			yield scrapy.Request (self.rootUrl + x, self.parseProductDetails, dont_filter=True)

	def parseGenerations (self, resp):
		for x in resp.xpath ('//div[contains(@class, "category-view")]/div/div/h2/a/@href').extract():
			yield scrapy.Request (self.rootUrl + x, self.parseTrims, dont_filter=True)

	def parseTrims (self, resp):
		for x in resp.xpath ('//h2/a/@href').extract():
			yield scrapy.Request (self.rootUrl + x, self.parseProducts, dont_filter=True)


	def parseProducts (self, resp):
		productsByCar = resp.xpath ('//div[contains(@class, "row")]/div/div/div/a/@href').extract()
		for x in productsByCar:
			yield scrapy.Request (self.rootUrl + x, self.parseProductDetails, dont_filter=True)

	def parseProductDetails (self, resp):
		breadCrumbs = resp.xpath ('//div[contains (@class, breadcrumbs)]/a/text()').extract()
		price = resp.xpath ('//span[contains (@class, "PricepriceWithoutTax")]/text()').extract()[0]

		scrapItem = tuningItem()
		scrapItem['makeModelString'] = ' '.join (set(filter (lambda item: not any(x for x in self.disallowedFields if x in item.lower()), breadCrumbs))).strip()
		scrapItem['sku'] = resp.xpath ('//sku/text()').extract()[0].replace('SKU:', '').strip()
		scrapItem['media'] = [{'type': 'image', 'link': self.rootUrl + x} for x in resp.xpath ('//img[contains(@class, "product-image")]/@src').extract()]
		scrapItem['title'] = resp.xpath ('//h1[contains (@class, "prod")]/text()').extract()[0]

		scrapItem['price'] = parseFloat (price)
		scrapItem['description'] = ' '.join ([re.sub (r'[^0-9a-zA-Z\s]+', '', x ) for x in resp.xpath ('//span[contains (@itemprop, "description")]/p/span/text()').extract() + resp.xpath ('//span[contains (@itemprop, "description")]/p/text()').extract()]).strip()
		scrapItem['url'] = resp.url
		return scrapItem


class WeistecSpider (scrapy.Spider):
	name="weistec"
	def start_requests (self):
		return [scrapy.Request ('http://weistec.com/', callback=self.parseGenerationTrim)]

	def parseGenerationTrim (self, resp):
		genTrimUrls = filter (lambda item: 'suv' not in item and len(item.split('/')) == 8 or len(item.split('/')) > 8,  resp.xpath ('//li[contains(@class, "level2")]//a/@href').extract())
		for link in genTrimUrls:
			yield scrapy.Request (link, callback=self.parseProducts)

	def parseProducts (self, resp):
		productLinks = resp.xpath ('//a[contains(@class, "product-image")]/@href').extract()
		for x in productLinks:
			yield scrapy.Request (x, callback=self.parseProductDetails)

	def parseProductDetails (self, resp):
		scrapItem = tuningItem()
		breadCrumbs = filter(lambda item:'suv' not in item.lower(), resp.xpath ('//div[contains(@class, "breadcrumbs")]//a//text()').extract()[2:-1])
		priceField  = filter(lambda item: len (item.strip()) > 0, resp.xpath ('//span[contains(@class, "price")]//text()').extract())
		if (len (priceField) > 0):
			scrapItem['price'] = parseFloat (priceField[0])
		else:
			scrapItem['price'] = None
		scrapItem['makeModelString'] =  'Mercedes-Benz ' + breadCrumbs[0] + '-class ' + ' '.join (breadCrumbs[1:])
		scrapItem['sku'] = resp.xpath ('//p[contains(@class, "sku")]/text()').extract()[0]
		scrapItem['title'] = resp.xpath ('//div[contains(@class, "product-name")]/h1/text()').extract()[0]
		scrapItem['media'] = [{'type': 'image', 'link': x } for x in resp.xpath ('//p[contains (@class, "product-image")]//img/@src').extract() + resp.xpath ('//div[contains (@class, "more-views")]//a/@href').extract()]
		scrapItem['description'] = parseContent (resp.xpath ('//div[contains (@class, "std")]//text()').extract())
		scrapItem['url'] = resp.url
		return scrapItem


class HennesseySpider (scrapy.Spider):
	name='hennessey'

	modelNameSelector='//div/p//a//text()'
	modelLinkSelector='//div/p//a//@href'

	packageLinkSelector='//div//a//@href'
	packageStringSelector='//div//a//text()'

	breadCrumbsSelector='//div[contains(@class, breadcrumbs_inner)]/a/text()'
	currentCrumbSelector='//div[contains(@class, breadcrumbs_inner)]/span[contains(@class, "current")]/text()'

	allowed_domains = ['hennesseyperformance.com']

	def start_requests (self):
		return [scrapy.Request ('http://www.hennesseyperformance.com/vehicles/', callback=self.parseMakes)]
	def parseMakes (self, resp):
		makes = resp.xpath ('//div[contains (@class, "wpb_wrapper")]/a/@href').extract()
		yield scrapy.Request('http://www.hennesseyperformance.com/vehicles/cadillac/ats-v/2016-cadillac-ats-v/',
							callback=self.parseIndexPage)
		for link, idx in izip(makes, xrange (len (makes))):
			req = scrapy.Request (link, callback=self.parseIndexPage)
			req.meta['idx'] = idx
			yield req
	def parseIndexPage (self, resp):
		# scrapItem = tuningItem()
		# scrapItem = projectItem()
		images = [x[:x.find ('?fit')] for x in resp.xpath ('//div[contains (@class, "gallery_holder")]//img/@src').extract()]
		breadCrumbs = filter (lambda item: len (item.strip()), resp.xpath (self.breadCrumbsSelector).extract())
		currentCrumb = filter (lambda item: len (item.strip()), resp.xpath (self.currentCrumbSelector).extract())

		if currentCrumb and currentCrumb[0].find ('Upgrade') > 0:
			if currentCrumb[0] == '2017 Acura NSX':
				return
			scrapItem = projectItem()
			scrapItem['makeModelString'] = parseContent (breadCrumbs[4:6])
			scrapItem['description'] = parseContent (currentCrumb)
			scrapItem['media'] = [{'type': 'image', 'link': x } for x in images]
			scrapItem['projectItems'] = parseAlnum (resp.xpath ('//div[contains (@class, "wpb_wrapper")]//p//text()').extract())
			scrapItem['url'] = resp.request.url
			# scrapItem['price'] = None
			# print scrapItem
			yield scrapItem
		else:
			modelLinks = resp.xpath (self.modelLinkSelector).extract()[:-2]
			modelStrings = resp.xpath (self.modelNameSelector).extract()[:-2]
			for modelLink, modelString in izip(modelLinks, modelStrings):
				if 'hennesseyperformance' in modelLink:
					req =  scrapy.Request (modelLink, callback=self.parseIndexPage)
					req.meta['makeModelString'] = modelString
					yield req


class AzeurosSpider (scrapy.Spider):
	name='azeuros'
	rootUrl='http://azeuros.com'

	indexListingsSelector='//div[contains(@class, "wpb_wrapper")]//a[contains(@class, "linkrow")]/@href'
	listingMediaSelector = '//img[contains(@class, "attachment-full")]/@src'
	makeModelStringSelector = '//div[contains(@class, "showroom-txt-wrapper")]/h3/text()'
	priceStringSelector = '//div[contains(@class, "showroom-txt-wrapper")]/h3/text()'
	spanSelector = '//div[contains(@class, "showroom-txt-wrapper")]/p[contains (@class, "showroom-txt")]/text()'
	def start_requests (self):
		yield scrapy.Request (self.rootUrl + '/showroom', callback=self.parseListingsIndexPage)

	def parseListingsIndexPage (self, resp):
		listingLinks = resp.xpath (self.indexListingsSelector).extract()
		for link in listingLinks:
			print link
			yield scrapy.Request (self.rootUrl + link, callback=self.parseListingPage)

	def parseListingPage (self, resp):
		scrapItem = listingItem()
		scrapItem['media'] = parseMedia ('image', resp.xpath (self.listingMediaSelector).extract())
		try:
			prices = [ parseFloat (x) for x in resp.xpath (self.priceStringSelector).extract()]
			scrapItem['price'] = prices[:-1][0]
		except:
			scrapItem['price'] = None
		# scrapItem['price'] = filter (lambda item: item !== None, )
		spanTexts = resp.xpath (self.spanSelector).extract()
		scrapItem['mileage'] = parseFloat (spanTexts[0])
		try:
			scrapItem['carFax'] = filter (lambda item: item.find('carfax') > -1, resp.xpath ('//div[contains(@class, "showroom-txt-wrapper")]//a/@href').extract())[0]
			scrapItem['vin'] = re.findall (r'vin=\w+', scrapItem['carFax'])[0].replace ('vin=','')
		except:
			scrapItem['carFax'] = None
			scrapItem['vin'] = None

		scrapItem['makeModelString'] = resp.xpath (self.makeModelStringSelector).extract()[0]
		scrapItem['description'] = parseContent(spanTexts[1:])
		scrapItem['url'] = resp.url
		print (scrapItem)
		yield (scrapItem)


class ACGSpider (scrapy.Spider):
	name='acg'
	rootUrl='http://www.acgautomotive.com'
	dealerEmail = 'james@acgautomotive.com'
	dealerPhone = '+1(858)633-1017'
	dealerLogo = 'http://www.acgautomotive.com/wp-content/themes/acg/images/acg-logo.png'
	dealerName = 'ACG Automotive'
	dealerAddress = '7884 Ronson Road'
	dealerCity =  'San Diego'
	dealerState = 'CA'
	dealerZip =  '92111'

	def start_requests (self):
		yield scrapy.Request (self.rootUrl + '/projects/', self.parseProjectIndexPage)

	def parseProjectIndexPage (self, resp):
		projectCarLinks = resp.xpath ('//div[contains (@class, "project_box_info")]/a//@href').extract()
		for link in projectCarLinks:
			yield scrapy.Request (link, self.parseProjectDetails)

	def parseProjectDetails (self, resp):
		scrapItem = projectItem()
		scrapItem['makeModelString'] = resp.xpath ('//div[contains(@class, "project_container")]//h3//text()').extract()[0]
		scrapItem['description'] = parseContent (resp.xpath ('//div[contains (@class, "project_content")]//ul/li/text()').extract())
		scrapItem['projectItems'] = parseAlnum (resp.xpath ('//div[contains (@class, "project_content")]//ul/li/text()').extract())
		scrapItem['media'] = parseMedia ('image', resp.xpath ('//div[contains (@class, "project_img_slider")]/ul/li/img/@src').extract())
		scrapItem['url'] = resp.url

		scrapItem['dealerEmail'] = self.dealerEmail
		scrapItem['dealerPhone'] = self.dealerPhone
		scrapItem['dealerLogo'] = self.dealerLogo
		scrapItem['dealerName'] = self.dealerName

		scrapItem['dealerAddress'] = self.dealerAddress
		scrapItem['dealerCity'] = self.dealerCity
		scrapItem['dealerState'] = self.dealerState
		scrapItem['dealerZip'] = self.dealerZip

		print scrapItem
		yield scrapItem


class GMGSpider (scrapy.Spider):
	name='gmg'
	rootUrl='https://www.gmgracing.com/project/'
	indexLvlLinks = '//div[contains (@class, "post-thumbnail")]//a/@href'
	projectItemTitleSelector = '//table//label/text()'
	projectItemsSelector = '//table//td/text()'
	makeModelStringSelector = '//h2[contains(@class, "post-title")]/text()'
	mediaSelector = '//div[contains (@class, "cycle-slideshow")]/img/@src'
	descriptionSelector = '//div[contains (@class, "post-content")]/p/text()'
	def start_requests (self):
		yield scrapy.Request (self.rootUrl, self.parseIndexPage)

	def parseIndexPage (self, resp):
		for link in resp.xpath (self.indexLvlLinks).extract():
			yield scrapy.Request (link, self.parseProjectDetails)

	def parseProjectDetails (self, resp):
		scrapItem = projectItem()
		scrapItem['makeModelString'] = parseFirst (resp.xpath (self.makeModelStringSelector))
		scrapItem['description'] = parseFirst (resp.xpath (self.descriptionSelector))
		itemTitle = parseAlnum (resp.xpath (self.projectItemTitleSelector).extract()) [1:]
		itemDetails = parseAlnum (resp.xpath (self.projectItemsSelector).extract()) [1:]
		scrapItem['projectItems'] = [title + ': ' + description for title, description in izip (itemTitle, itemDetails)]
		scrapItem['media'] = parseMedia ('image', resp.xpath (self.mediaSelector).extract())
		scrapItem['url'] = resp.url
		yield scrapItem
		print scrapItem


class iPESpider (scrapy.Spider):
	name='ipe'
	rootUrl='http://www.ipe-f1.com'
	indexLvlLinks='//li[contains (@id, "li-level-2")]/a/@href'
	makeSelector = '//div[contains(@class, "tableone")]//th[contains(@class, "secondcolumn")]//li/text()'
	makeModelStringSelector = '//div[contains (@class, "tableone")]//th[contains(@class, "secondcolumn")]/text()'
	projectImagesSelector = '//li//span[contains (@class, "sigProLinkWrapper")]/a/@href'
	projectDescriptionSelector = '//div[contains (@class, "itemFullText")]//p/text()'

	itemsImageSelector = '//div[contains(@class, "ai_content")]//a/@href'
	itemsDescriptionSelector = '//div[contains(@class, "ai_title")]//h3/text()'
	itemsSKUSelector = '//div[contains(@class, "ai_itemno_head")]/p/text()'

	youtubeSelector = '//div[contains(@class, "item_videos")]//a/@href'
	def start_requests (self):
		yield scrapy.Request (self.rootUrl + '/index.php/en-GB', self.parseIndexLinks)

	def parseIndexLinks (self, resp):
		for x in resp.xpath (self.indexLvlLinks).extract():
			yield scrapy.Request (self.rootUrl + x, self.parseProductDetails)

	def parseProductDetails (self, resp):
		print resp.url
		scrapProjectItem = projectItem()
		scrapTuningItem = tuningItem()
		make = resp.xpath (self.makeSelector).extract_first().strip()
		yearRange = resp.xpath (self.makeModelStringSelector).extract()[-2].strip()
		modelDescription = parseContent (resp.xpath (self.makeModelStringSelector).extract()[:-2])

		projectImages = parseMedia('image', list(set([self.rootUrl + x for x in resp.xpath (self.projectImagesSelector).extract()])))
		projectDescription = parseContent (resp.xpath (self.projectDescriptionSelector).extract())

		projectItemImages = [self.rootUrl + x for x in resp.xpath (self.itemsImageSelector).extract ()]
		projectItemDescriptions = resp.xpath (self.itemsDescriptionSelector).extract()
		projectSKUs = resp.xpath (self.itemsSKUSelector).extract()

		scrapProjectItem['makeModelString'] = yearRange + " " + make + " " + modelDescription
		scrapProjectItem['media'] = projectImages
		scrapProjectItem['description'] = projectDescription
		scrapProjectItem['url'] = resp.url
		scrapProjectItem['projectItems'] = list()
		for imageUrl, description, sku in izip (projectItemImages, projectItemDescriptions, projectSKUs):
			scrapTuningItem = tuningItem()
			scrapTuningItem['makeModelString'] = scrapProjectItem['makeModelString']
			scrapTuningItem['title'] = description.strip()
			scrapTuningItem['sku'] = sku.replace ('(', '').replace (')', '').strip()
			scrapTuningItem['media'] = parseMedia ('image',[imageUrl])

			scrapProjectItem['projectItems'].append (scrapTuningItem['title'] + ' ' + scrapTuningItem['sku'] )
			# yield scrapTuningItem
		scrapProjectItem['media'] = scrapProjectItem['media'] +  parseMedia('video',resp.xpath (self.youtubeSelector).extract())
		yield scrapProjectItem


class RenntechListingsSpider (scrapy.Spider):
	name='renntechListings'
	rootUrl='http://www.renntechmercedes.com'

	indexLinksSelector = '//p/a/@href'
	mediaSelector = '//div[contains(@class, "item-page")]/table//div[contains(@class,  "jsn-gallery")]//img/@src'
	detailsSelector = '//div[contains (@class, "item-page")]/table/tr[3]//text()'
	makeModelStringSelector = '//div[contains(@class, "item-page")]/table//tr[3]//text()'
	descriptionSelector = '//div[contains(@class, "item-page")]/table//tr[4]//p/text()'
	itemsSelector = '//div[contains(@class, "item-page")]/table//tr[4]//li/text()'
	def start_requests (self):
		# yield scrapy.Request (self.rootUrl + '/index.php/customer/vehicles-for-sale', self.parseIndexLinks)
		yield scrapy.Request ('http://www.renntechmercedes.com/index.php/customer/vehicles-for-sale/12-cars-for-sale/40-for-sale-e-60', self.parseListingPage)

	def parseIndexLinks (self, resp):
		for link in resp.xpath (self.indexLinksSelector).extract():
			yield scrapy.Request (self.rootUrl + link, self.parseListingPage)

	def parseListingPage (self, resp):
		scrapItem = projectItem()
		scrapItem['description'] = parseContent (resp.xpath (self.detailsSelector).extract())
		scrapItem['media'] = parseMedia ('image', resp.xpath (self.mediaSelector).extract())
		scrapItem['url'] = resp.url
		scrapItem['makeModelString'] = filter (lambda item: re.search (r'\b19[0-9][0-9] Mercedes', item), resp.xpath (self.makeModelStringSelector).extract() )[0].replace ('Vehicle: ', '')
		scrapItem['projectItems'] = parseAlnum (resp.xpath (self.itemsSelector).extract())
		yield scrapItem


class ClassicRecreationSpider (scrapy.Spider):
	name='classicRecreations'
	rootUrl = 'http://www.classic-recreations.com/'
	start_urls = [rootUrl]

	blackList = [':']
	indexModelsSelector = '//ul[contains (@id, "MegaMenu")]/li[2]//@href'
	imgPrefix = 'http://www.classic-recreations.com/wp-content/plugins/easy-media-gallery-pro/includes/class/timthumb.php?src='
	makeModelStringSelector = '//h1[contains (@class, "pageTitle")]//text()'
	descriptionSelector = '//div[contains (@class, "contentArea")]/p[0]/span/text()'
	optionsUrlSelector = '//div[contains (@align, "center")]'
	itemsSelector = '//div[contains(@class, "half_page")]//span//text()'
	def parse (self, resp):
		for link in resp.xpath (self.indexModelsSelector).extract():
			yield scrapy.Request (link, self.parseListingPage)

	def parseListingPage (self, resp):
		scrapItem = projectItem()
		images = list(set([ x.replace (self.imgPrefix, '') for x in filter (lambda item: re.search ('jpg', item), resp.xpath('//a/@href').extract())]))
		scrapItem['media'] = parseMedia ('image', images)
		scrapItem['makeModelString'] = 'Ford Mustang ' +  resp.xpath (self.makeModelStringSelector).extract_first()
		scrapItem['description'] = resp.xpath (self.descriptionSelector).extract_first()
		scrapItem['projectItems'] = parseAlnum (filter (lambda item: re.search (r':$', item.strip())==None and len(item.strip()), resp.xpath (self.itemsSelector).extract())[1:])
		scrapItem['url'] = resp.url
		yield scrapItem
		# optionsUrl = filter (lambda item: re.search('build-options', item), resp.xpath ('//a/@href').extract())[0]
		# optionsReq = scrapy.Request (optionsUrl, self.parseOptions)
		# optionsReq.meta['scrapItem'] = scrapItem
		# yield optionsReq

	# def parseOptions (self, resp):


class CobbSpider (scrapy.Spider):
	name='cobb'
	start_urls = ['http://www.cobbtuning.com/products']
	indexLvlLinksSelector = '//div[contains(@class, "product--list")]/a/@href'
	modelsLinksSelector = '//div[contains (@class, "model--items")]/a/text()'
	titleSelector = '//h1[contains(@class, "product--heading")]//text()'
	descriptionSelector = '//p[contains(@class, "accordion--simple__article")]//text()'
	mediaSelector = '//div[contains(@class, "accordion--simple")]//img/@src'
	priceSelector = '//div[contains(@class, "wrapper--large")]//h5[contains(@class, "product--heading")]/text()'

	def parse (self, resp):
		for link in resp.xpath (self.indexLvlLinksSelector).extract():
			yield scrapy.Request (link, self.parseProducts)

	def parseProducts (self, resp):
		for link in resp.xpath (self.indexLvlLinksSelector).extract():
			yield scrapy.Request (link, self.parseProductDetails)

	def parseProductDetails (self, resp):
		matchingModels = resp.xpath (self.modelsLinksSelector).extract()
		title = resp.xpath (self.titleSelector).extract_first()
		description = parseContent (resp.xpath (self.descriptionSelector).extract())
		media = parseMedia ('image', resp.xpath (self.mediaSelector).extract())
		price = parseFloat (resp.xpath (self.priceSelector).extract_first().encode ('ascii', 'ignore'))

		for model in matchingModels:
			scrapItem = tuningItem ()
			scrapItem['makeModelString'] = model
			scrapItem['title'] = title
			scrapItem['description'] = description
			scrapItem['price'] = price
			scrapItem['media'] = media
			scrapItem['url'] = resp.url
			yield scrapItem


class RoushProjectSpider (scrapy.Spider):
	name='roushProjects'
	start_urls = ['http://www.roushperformance.com/vehicles/']
	rootUrl = 'http://www.roushperformance.com'

	indexLvlLinksSelector = '//div[contains (@class, "vehicle")]//a/@href'
	mediaSelector = '//img/@src'
	descriptionSelector = '//ul[contains (@class, "component_list")]//span/text()'
	makeModelStringSelector = '//div[contains (@class, "title")]/span/text()'

	def parse (self, resp):
		for link in list (set(resp.xpath (self.indexLvlLinksSelector).extract())):
			if not re.search ('archive', link):
				yield scrapy.Request (link, self.parseProductDetails)

	def parseProductDetails (self, resp):
		scrapItem = projectItem()
		images = [self.rootUrl + link for link in resp.xpath (self.mediaSelector).extract()]
		title = resp.xpath (self.makeModelStringSelector).extract_first()
		scrapItem['makeModelString'] = 'Ford ' + title
		scrapItem['media'] = parseMedia ('image', filter (lambda item: re.search('vehicles', item), images))
		scrapItem['projectItems'] = parseAlnum (resp.xpath (self.descriptionSelector).extract())
		scrapItem['url'] = resp.url
		yield scrapItem
