import scrapy

class image_doc (scrapy.Item):
    label = scrapy.Field()
    image_urls = scrapy.Field()
    ext = scrapy.Field()
    int_parts = scrapy.Field()
