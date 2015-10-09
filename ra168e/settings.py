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


MONGODB_URI = 'mongodb://' + os.environ['VEHICLE_DATA_PORT_27017_TCP_ADDR'] + ':' + os.environ['VEHICLE_DATA_PORT_27017_TCP_PORT']

MONGODB_DATABASE = 'fine_scrap'
MONGODB_COLLECTION = 'urls'
IMAGES_STORE = "/home/ubuntu/fine_scrap"

MONGODB_BUFFER_DATA = 10
CONCURRENT_REQUESTS = 3
DOWNLOAD_DELAY = 1 


