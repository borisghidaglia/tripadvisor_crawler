# -*- coding: utf-8 -*-
from scrapy import Request, Spider
from ..items import Attraction, AttractionReview
from ..utils import get_d_values, get_g_values, TripadvisorMongoDB

class TripadvisorAttractionSpider(Spider):
    """ Crawl all the attractions indexed by their d_values in the file data.py

    The g_values_to_crawl object could be a list of int, a range() of some value or anything else as long as
    it's iterable and contains int
    """
    name='tripadvisor_attraction'
    allowed_domains = ['tripadvisor.fr']

    def start_requests(self):
        for i in get_g_values():
            link = "https://tripadvisor.fr/Attraction_Review-g%s"%i
            yield Request(link, callback=self.parse_attractions, meta={ 'g_value':i })

    def parse_attractions(self, response):
        name = response.xpath('//*[@id="HEADING"]/text()').extract()[0]\
            .replace(' : les meilleures activités', '')\
            .replace('\n', '')\
            .replace('\u200e', '')
        g_value = response.meta['g_value']
        yield Attraction(
            name = name,
            g_value = g_value
        )


class TripadvisorAttractionReviewSpider(Spider):
    name='tripadvisor_attraction_review'
    allowed_domains = ['tripadvisor.fr']

    def __init__(self, category=None, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.attractions = TripadvisorMongoDB().get_collection('tripadvisor_attraction')

    def start_requests(self):
        """ For each attraction in database, start crawling the attraction_review indexed by their
        d_values in the "d_values_by_attraction.json" file
        """
        for attraction in self.attractions:
            d_values = get_d_values(attraction['name'])
            if d_values:
                for d_value in d_values:
                    link = "https://www.tripadvisor.fr/Attraction_Review-g%s-d%s"%(attraction['g_value'], d_value)
                    yield Request(
                        link,
                        callback = self.parse_attraction_review,
                        meta = {
                            'g_value' : attraction['g_value'],
                            'd_value' : d_value
                        }
                    )

    def parse_attraction_review(self, response):
        name = response.xpath('//*[@id="HEADING"]/text()').extract()[0]
        yield AttractionReview(
            name = name,
            g_value = response.meta['g_value'],
            d_value = response.meta['d_value']
        )



class TripadvisorSpider(Spider):
    name = 'tripadvisor'
    allowed_domains = ['tripadvisor.fr']
    start_urls = ['https://tripadvisor.fr/Attraction_Review-g187147-d188151-Reviews-Eiffel_Tower-Paris_Ile_de_France.html']

    def parse(self, response):
        # ids = response.xpath('//*[@class="member_info"]/div/@id').extract()
        # for id in ids:
        #     print(id)
        nb_pages = int(response.xpath('//*[@id="taplc_location_reviews_list_resp_ar_responsive_0"]/div/div[15]/div/div/div/a[8]/text()').extract()[0])
        for i in range(0, 10):
            link = "https://www.tripadvisor.fr/Attraction_Review-g187147-d188151-Reviews-or%s-Eiffel_Tower-Paris_Ile_de_France.html"%(i*10)
            yield Request(link, callback=self.parse_comments)

    def parse_comments(self, response):
        html_ids = response.xpath('//*[@class="member_info"]/div/@id').extract()
        for html_id in html_ids:
            [uid, src] = html_id.replace('UID_','').replace('SRC_','').split('-')
            print(uid, src)
