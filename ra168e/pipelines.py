import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
class MongoDBPipeline(object):
	def __init__(self):
		connection = pymongo.MongoClient(
		settings['MONGODB_URI'],
		)
		db = connection[settings['MONGODB_DATABASE']]
		self.collection = db[settings['MONGODB_COLLECTION']]
	def process_item(self, item, spider):
		self.collection.insert(dict(item))
		return item