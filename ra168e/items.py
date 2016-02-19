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
    ext = scrapy.Field()
    int_parts = scrapy.Field()


class zipcity (scrapy.Item):
    city = scrapy.Field()
    zipcode = scrapy.Field()

class listing_item (scrapy.Item):
    colors = scrapy.Field()
    dealer = scrapy.Field()
    listedSince = scrapy.Field()
    make = scrapy.Field()
    mileage = scrapy.Field()
    model = scrapy.Field()
    options = scrapy.Field()
    photos = scrapy.Field()
    prices = scrapy.Field()
    stockNumber = scrapy.Field()
    styleId = scrapy.Field()
    trim = scrapy.Field()
    vin = scrapy.Field()
    year = scrapy.Field()

class dealer_item (scrapy.Item):
    dealerId = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    franchiseId = scrapy.Field()
    contactInfo = scrapy.Field()
