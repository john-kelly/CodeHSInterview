from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import log

from scrapy.shell import inspect_response
from bs4 import BeautifulSoup
from CodeHSWikiBot.items import *

import re

class WikiSpider(Spider):
    name = "wikispider"
    
    #http://blog.codinghorror.com/parsing-html-the-cthulhu-way/
    #the struggle is real

    #Handled edge cases:
    #https://en.wikipedia.org/wiki/Aware_Electronics#References -> toc
    #http://en.wikipedia.org/wiki/Behavior -> wikionary links
    #https://en.wikipedia.org/wiki/Delaware -> IPA
    #https://en.wikipedia.org/wiki/Security -> loops
    #https://en.wikipedia.org/wiki/pokemon -> just cuz
    
    #Known problems:
    #https://en.wikipedia.org/wiki/List_of_intelligence_gathering_disciplines -> lists
    #https://en.wikipedia.org/wiki/Study -> lists
    #https://en.wikipedia.org/wiki/Earth -> skips bold links
    
    def start_requests(self):
        request = Request(url=self.start_urls[0],
                        callback=self.parse_page)
        wiki_item = WikiItem()
        
        wiki_item['path'] = [self.start_urls[0]]
        wiki_item['num_hops'] = 0
        
        request.meta['item'] = wiki_item

        return [request]

    def parse_page(self,response):        

        if('en.wikipedia.org/wiki/Philosophy' in response.url):
            the_item = response.meta['item']
            for elem in the_item['path']:
                print(elem)
            print("Total Number of Hops: " + str(the_item['num_hops']))
            return 
        

        # #BeautifulSoup
        # ############################################################
        # main_content = response.xpath('//div[@id="mw-content-text"]')[0].extract()
        # soup = BeautifulSoup(main_content)
        
        # Preprocessing
        # while(soup.i):
        #     soup.i.extract()
        # while(soup.span):
        #     soup.span.extract()
        # while(soup.sup):
        #     soup.sup.extract()
        # while(soup.table):
        #     soup.table.extract()
        # for elem in soup.find_all("div", class_="hatnote"):
        #     elem.extract()
        # for elem in soup.find_all("a", class_="image"):
        #     elem.extract()
        # #Pray for the first link
        # first_link = soup.a['href']
        # #############################################################
    
        # Regex :/
        #############################################################
        p_index = 1
        while True:
            try:
                if p_index > 5:
                    print("Sorry, Wikipedia is irregular at times.")
                    return
                    #can fix this
                    # main_content_sel = response.xpath('//div[@id="mw-content-text"]')[0]
                    # first_link = main_content_sel.xpath('./a/@href')[0].extract()
                    # print("We took a risk")

                main_content_sel = response.xpath('//div[@id="mw-content-text"]/p['+str(p_index)+']')[0]
                
                string = main_content_sel.extract()
            
                #filter IPA (Could be causing a problem with STUDY page)
                filtered = re.sub('\(<span [^>]*?>.*?<\/span>\)',"",string)
            
                #filter links surrounded by ()'s
                filtered = re.sub('\([^)]*?<a[^>]*?>[^<]*?<\/a>[^)]*?\)',"",filtered)

                #filter wikionary links
                filtered = re.sub('<a href="\/\/en\.wiktionary\.org\/wiki\/.*?<\/a>',"",filtered)   
            
                #convert filtered text to Selector for easy xpath selection
                selector = Selector(response=None, text=filtered, type="html")
                
                #dont have to worry about <i> links b/c this skips them!
                first_link = selector.xpath('./body/p/a/@href')[0].extract()

                break
            except:
                p_index += 1      
        ################################################################

        request = Request(
           url='https://en.wikipedia.org' + first_link,
           callback=self.parse_page)
        
        wiki_item = response.meta['item']
        wiki_item['path'].append(str('http://en.wikipedia.org' + first_link))
        wiki_item['num_hops'] += 1 
        request.meta['item'] = wiki_item
        
        return request