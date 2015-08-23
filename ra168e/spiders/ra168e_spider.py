import scrapy, re, os, json, pickle
from itertools import product, izip
from ra168e.items import image_doc
from pymongo import MongoClient
mongo_host_name = 'localhost'
mongo_port = 27017

client = MongoClient(mongo_host_name, mongo_port)

vehicle_data_db = client['vehicle_data']

class images (scrapy.Spider):
	name = "images"
	start_urls = ["http://www.goldpriceoz.com/gold-price-per-kilo/"]
	# images_urls_path = "/home/ubuntu/ra168e/ra168e/urls_source.p"
	images_urls_path = "/Users/bski/Project/image_training/ra168e/ra168e/urls_source.p"
	def parse(self, response):
		images_source = pickle.load (open(self.images_urls_path, "rb"))
		for x, y in images_source.items():
			car_images = image_doc()
			car_images["label"] = x
			car_images["image_urls"] = y
			yield car_images
