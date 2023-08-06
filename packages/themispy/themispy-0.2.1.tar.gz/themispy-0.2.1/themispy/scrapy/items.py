# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FileDownloader(scrapy.Item):
    """Scrapy Item Class defined for downloading files.
    
    Attributes:
        file_urls (scrapy.Field): this attribute holds the URL of the
    file that will be downloaded.
        files (scrapy.Field): register the status of the downloading
    process.
        
    """
    file_urls = scrapy.Field() # Do not rename this!
    files = scrapy.Field() # Do not rename this!
