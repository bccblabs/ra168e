import os

BOT_NAME = 'ra168e'

SPIDER_MODULES = ['ra168e.spiders']
NEWSPIDER_MODULE = 'ra168e.spiders'
LOG_LEVEL="INFO"
LOG_FILE="pure_images.log"
ITEM_PIPELINES = {
	'scrapy_mongodb.MongoDBPipeline': 90,
 	'ra168e.pipelines.DownloadClassifyPipeline': 1
}

USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0) Gecko/16.0 Firefox/16.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10'
]

MONGODB_URI = 'mongodb://' + "localhost" + ':' + "27017"
MONGODB_COLLECTION = 'images'
MONGODB_DATABASE = 'pure_images2'
MONGODB_BUFFER_DATA = 1
CONCURRENT_REQUESTS = 15 
DOWNLOAD_DELAY = 1
IMAGES_STORE = "/home/ubuntu/pure_images2"

