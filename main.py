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
    *termcolor 1.1.0

"""

import asyncio
import logging
from src import crawler, utils, scraper
from pprint import pprint

from PyInquirer import style_from_dict, Token, prompt, Separator
from pyfiglet import Figlet
from termcolor import colored

#Scraper = sc
#Crawler = cw


def main():
 
    try:
        logging.basicConfig(filename='loggings.log', 
        level=logging.INFO, 
        format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
        logging.info("\n-------------------------------------------------------------------------------------------------\n")
        logging.info("CRAWLER STARTS")
        vendors = utils.readFileToArray("vendors.txt")
        products = utils.readFileToArray("products.txt")
        excludedWords = utils.readFileToArray("excludedWords.txt")
        asyncio.run(crawler.init_crawler(products,vendors,excludedWords))
        logging.info("CRAWLER ENDS")

        utils.vendor_folder_mapping()
        utils.product_folder_mapping(vendors)
        logging.info("SCRAPER STARTS")
        asyncio.run(scraper.scraper_init(vendors,products))
        logging.info("SCRAPER ENDS")
        utils.cleanUp(vendors)
        logging.info("\n-------------------------------------------------------------------------------------------------\n")

    except Exception as identifier:
        logging.critical("ERROR IN MAIN : "+str(identifier))
    
main()
exit(0)