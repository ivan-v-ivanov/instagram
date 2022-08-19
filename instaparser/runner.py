from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from instaparser.spiders.instagram import UserFirstSpider
from instaparser.spiders.instagram_another_user import UserSecondSpider
from instaparser import settings

if __name__=='__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(UserFirstSpider)
#    process.crawl(UserSecondSpider)

    process.start()