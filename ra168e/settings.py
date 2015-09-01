import os

BOT_NAME = 'ra168e'

SPIDER_MODULES = ['ra168e.spiders']
NEWSPIDER_MODULE = 'ra168e.spiders'

ITEM_PIPELINES = {
	'ra168e.middlewares.RandomUserAgentMiddleware': 400,
	'scrapy_mongodb.MongoDBPipeline': 90,
}


MONGODB_URI = 'mongodb://' + os.environ['VEHICLE_DATA_PORT_27017_TCP_ADDR'] + ':' + os.environ['VEHICLE_DATA_PORT_27017_TCP_PORT']
MONGODB_COLLECTION = 'image_urls'
MONGODB_BUFFER_DATA = 10
CONCURRENT_REQUESTS = 1 
DOWNLOAD_DELAY = 2
MONGODB_DATABASE = 'pure_urls'

