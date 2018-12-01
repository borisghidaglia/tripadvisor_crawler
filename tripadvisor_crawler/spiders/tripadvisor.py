# -*- coding: utf-8 -*-
from scrapy import Request, Spider


class TripadvisorSpider(Spider):
    name = 'tripadvisor'
    allowed_domains = ['tripadvisor.fr']
    start_urls = ['https://tripadvisor.fr/Attraction_Review-g187147-d188151-Reviews-Eiffel_Tower-Paris_Ile_de_France.html']

    def parse(self, response):
        # ids = response.xpath('//*[@class="member_info"]/div/@id').extract()
        # for id in ids:
        #     print(id)
        nb_pages = int(response.xpath('//*[@id="taplc_location_reviews_list_resp_ar_responsive_0"]/div/div[15]/div/div/div/a[8]/text()').extract()[0])
        for i in range(0, 10, 10):
            link = "https://www.tripadvisor.fr/Attraction_Review-g187147-d188151-Reviews-or%s-Eiffel_Tower-Paris_Ile_de_France.html"%i
            yield Request(link, callback=self.parse_users)

    def parse_comments(self, response):
        html_ids = response.xpath('//*[@class="member_info"]/div/@id').extract()
        for html_id in html_ids:
            [uid, src] = html_id.replace('UID_','').replace('SRC_','').split('-')
            print(uid, src)
