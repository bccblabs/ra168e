import scrapy, re, os, json, pickle
from itertools import product, izip
from ra168e.items import image_doc

class images (scrapy.Spider):
	name = "images"
	start_urls = ["http://www.goldpriceoz.com/gold-price-per-kilo/"]
	images_urls_path = "/home/ubuntu/ra168e/ra168e/"
	url_file = []
	def __init__(self, file_name):
		self.url_file = file_name
	def parse(self, response):
		images_source = pickle.load (open(self.images_urls_path + self.url_file, "rb"))
		for x, y in images_source.items():
			print x, len(y)
			car_images = image_doc()
			car_images["label"] = x
			car_images["image_urls"] = y[:10]
			yield car_images
