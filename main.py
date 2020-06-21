#-*- coding: UTF-8 -*-

"""
        e-commerce-crawler CLI
        Berkay KOÇAK - 2020 June

        CLI Web page crawler with scraper for e-commerce vendors.

Written with Python 3.7.3
Additional libraries:
    *Beautiful Soup 4.9^
    *PyInquirer
    *PyFiglet

"""

import asyncio
from src import crawler
import unicodedata


def main():
    
    #check if assets folder available, else create
    
    #ask for product name (it can be multiple like xx,aa,bb,cc...)
        

    #ask for words to exclude at search
    
    #check for scrape_elements.py file
        #show available vendors for crawling and scraping
    
    #with selected vendors, initialize crawling
    asyncio.run(crawler.init_crawler(["süpürge"],["teknosa","vatan"]))


main()