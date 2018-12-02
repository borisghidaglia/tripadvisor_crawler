# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Attraction(scrapy.Item):
    # Link to an Attraction :
    # https://www.tripadvisor.fr/Attractions-g{{g_value}}
    # ex : Paris has g_value=187147
    name = scrapy.Field()
    g_value = scrapy.Field()

class AttractionReview(scrapy.Item):
    # Link to an AttractionReview :
    # https://www.tripadvisor.fr/Attraction_Review-g{{g_value}}-d{{d_value}}
    # ex : Eiffel Tower has g_value=187147 and d_value=188151
    name = scrapy.Field()
    g_value = scrapy.Field()
    d_value = scrapy.Field()

class User(scrapy.Item):
    # @unique, tags, nb contribution, lieu de vie, nb de villes visitées,
    pass

class Review(scrapy.Item):
    # note, commentaire, lieu associé, contenu
    pass
