import scrapy

class vehicle_urls (scrapy.Item):
    images = scrapy.Field()
    image_urls = scrapy.Field()
    address =scrapy.Field()
    keywords = scrapy.Field()
    make = scrapy.Field()
    model = scrapy.Field()
    year = scrapy.Field()
    bodyType = scrapy.Field()
    listing_id = scrapy.Field()
    price = scrapy.Field()
    color_ext = scrapy.Field()
    color_int = scrapy.Field()
    transmission = scrapy.Field()
    mileage = scrapy.Field()
    restored = scrapy.Field()
    listing_url = scrapy.Field()


class zero_sixty (scrapy.Item):
    name = scrapy.Field()
    zs = scrapy.Field()

class major (scrapy.Item):
    title = scrapy.Field()
    fields = scrapy.Field()

class issues (scrapy.Item):
    name = scrapy.Field()
    recalls_cnt = scrapy.Field()
    investigations_cnt = scrapy.Field()
    complaints_cnt = scrapy.Field()
    tsbs_cnt = scrapy.Field()
    recall_stats = scrapy.Field()
    investigation_stats = scrapy.Field()
    complain_stats = scrapy.Field()
    investigations = scrapy.Field()
    recalls = scrapy.Field()

class entry (scrapy.Item):
    component = scrapy.Field()
    count = scrapy.Field()

class safety_entry (scrapy.Item):
    name = scrapy.Field()
    value = scrapy.Field()

class safety (scrapy.Item):
    ratings = scrapy.Field()
    equipments = scrapy.Field()
    photos = scrapy.Field()
    videos = scrapy.Field()
    name = scrapy.Field()
    major = scrapy.Field()