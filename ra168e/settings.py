import os

BOT_NAME = 'ra168e'

SPIDER_MODULES = ['ra168e.spiders']
NEWSPIDER_MODULE = 'ra168e.spiders'

LOG_LEVEL="INFO"
# LOG_FILE="listings.log"
ITEM_PIPELINES = {
	'scrapy_mongodb.MongoDBPipeline': 90,
}


MONGODB_URI = 'mongodb://localhost:27017'

MONGODB_DATABASE = 'listings'
MONGODB_COLLECTION = 'edmunds-ny'

MONGODB_BUFFER_DATA = 20
CONCURRENT_REQUESTS = 200


