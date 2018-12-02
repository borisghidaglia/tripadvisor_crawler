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


class TripadvisorReviewSpider(Spider):
    name = 'tripadvisor_review'
    allowed_domains = ['tripadvisor.fr']

    def __init__(self, category=None, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.attraction_reviews = TripadvisorMongoDB().get_collection('tripadvisor_attraction_review')

    def start_requests(self):
        for attraction_review in self.attraction_reviews:
            link = "https://www.tripadvisor.fr/Attraction_Review-g%s-d%s"%(attraction_review['g_value'], attraction_review['d_value'])
            yield Request(
                link,
                callback=self.parse_review_pages,
                meta={'attraction_review' : attraction_review}
            )

    def parse_review_pages(self, response):
        attraction_review = response.meta['attraction_review']
        nb_pages = int(response.xpath('//*[@id="taplc_location_reviews_list_resp_ar_responsive_0"]/div/div[15]/div/div/div/a[8]/text()').extract()[0])
        for i in range(0, 2):
            link = "https://www.tripadvisor.fr/Attraction_Review-g%s-d%s-Reviews-or%s-Eiffel_Tower-Paris_Ile_de_France.html"\
                %(attraction_review['g_value'], attraction_review['d_value'], i*10)
            yield Request(
                link,
                callback=self.parse_uid_and_src
            )

    def parse_uid_and_src(self, response):
        # Extracting titles, contents and grades
        titles = response.xpath('//*[@class="noQuotes"]/text()').extract()
        contents = response.xpath('//*[@class="partial_entry"]/text()').extract()
        # grades = response.xpath('//*[@class="ui_column"]')
        class_grades = response.xpath('//*[contains(@class,"ui_bubble_rating")]/@class').extract()
        grades = []
        for grade in class_grades:
            grades.append(int(grade.split(' ')[1].replace('bubble_', '')))
        print("################################################")
        print(titles)
        print("################################################")
        print(contents)
        print("################################################")
        print(grades)
        # for i in range(len(titles)):
        #     print(titles[i], contents[i], grades[i])
        # for title, content, grade in zip(titles, contents, grades):
        #     print(title, content, grade)
        # for html_id in html_ids:
        #     [uid, src] = html_id.replace('UID_','').replace('SRC_','').split('-')
        #     link = "https://www.tripadvisor.fr/MemberOverlay?uid=%s&c=&src=%s"\
        #         %(uid, src)
        #     yield Request(
        #         link,
        #
        #     )
