import scrapy


class tuningItem (scrapy.Item):
    name = scrapy.Field()
    sku = scrapy.Field()
    partId = scrapy.Field()
    description = scrapy.Field()
    details = scrapy.Field()
    specs = scrapy.Field()
    url = scrapy.Field()

    makeModelString = scrapy.Field()
    media = scrapy.Field()
    price = scrapy.Field()
