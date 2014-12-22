import sys
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from CodeHSWikiBot.spiders.WikiSpider import WikiSpider
from scrapy.utils.project import get_project_settings

#http://doc.scrapy.org/en/latest/topics/practices.html

if len(sys.argv) > 2:
	print(sys.argv)
	print("Expected only 1 argument, Please try again")
	exit()

spider = WikiSpider(start_urls=[sys.argv[1]])

settings = get_project_settings()
crawler = Crawler(settings)
crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
crawler.configure()
crawler.crawl(spider)
crawler.start()
log.start(loglevel=log.CRITICAL,logstdout=False)
reactor.run() # the script will block here until the spider_closed signal was sent