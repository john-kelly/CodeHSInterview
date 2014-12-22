from scrapy.dupefilter import RFPDupeFilter

class DupeFilter(RFPDupeFilter):
    """A dupe filter that considers the URL"""

    def log(self, request, spider):
        if self.logdupes:
            print("We encountered a loop! Try again next time")