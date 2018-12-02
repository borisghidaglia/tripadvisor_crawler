# -*- coding: utf-8 -*-
from scrapy import Request, Spider
from ..items import Attraction

class TripadvisorAttractionSpider(Spider):
    name='tripadvisor_attraction'
    allowed_domains = ['tripadvisor.fr']

    def start_requests(self):
        # g187147 is Paris
        for i in [187147]:
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
