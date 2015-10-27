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


MONGODB_URI = 'mongodb://localhost:27017'

MONGODB_DATABASE = 'pure_images7'
MONGODB_COLLECTION = 'urls'
IMAGES_STORE = "/home/ubuntu/pure_images6"

MONGODB_BUFFER_DATA = 1
CONCURRENT_REQUESTS = 5
DOWNLOAD_DELAY = 1


