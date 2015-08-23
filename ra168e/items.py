import scrapy

class image_doc (scrapy.Item):
    label = scrapy.Field()
    image_urls = scrapy.Field()
    images_path = scrapy.Field()
