import os

BOT_NAME = 'ra168e'

SPIDER_MODULES = ['ra168e.spiders']
NEWSPIDER_MODULE = 'ra168e.spiders'
LOG_LEVEL="INFO"
# LOG_FILE="scrap.log"
ITEM_PIPELINES = {
	'ra168e.middlewares.RandomUserAgentMiddleware': 400,
	'ra168e.middlewares.ProxyMiddleware': 410,
	'scrapy_mongodb.MongoDBPipeline': 90,
	'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
 	'scrapy.pipelines.images.ImagesPipeline': 1
}

USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0) Gecko/16.0 Firefox/16.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10'
]

# HTTP_PROXY = 'http://0.0.0.0:8123'

# MONGODB_COLLECTION = 'urls'
# MONGODB_BUFFER_DATA = 2
# CONCURRENT_REQUESTS = 3
# DOWNLOAD_DELAY = 2
# MONGODB_DATABASE = 'fine_scrap'
# MONGODB_URI = 'mongodb://' + os.environ['VEHICLE_DATA_PORT_27017_TCP_ADDR'] + ':' + os.environ['VEHICLE_DATA_PORT_27017_TCP_PORT']
MONGODB_URI = 'mongodb://localhost:27017'
IMAGES_STORE = '/pure_images'
# MONGODB_COLLECTION = 'issues_v2'
# MONGODB_DATABASE = 'vehicle_data'

MONGODB_COLLECTION = 'images'
MONGODB_DATABASE = 'pure_images'

MONGODB_BUFFER_DATA = 15
CONCURRENT_REQUESTS = 5
DOWNLOAD_DELAY = 3

