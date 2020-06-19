#-*- coding: UTF-8 -*-
import asyncio
from src import crawler
import unicodedata

def main():
    
    #check if assets folder available, else create
    
    #ask for product name (it can be multiple like xx,aa,bb,cc...)
        #convert special letters like ğ-ö to g-o
        #spcial_char_map = {ord('ä'):'a', ord('ü'):'u', ord('ö'):'o', ord('ş'):'s', ord('ç'):'c',ord('ğ'):'g'}
        #product.translate(spcial_char_map)
    
    #check for scrape_elements.py file
        #show available vendors for crawling and scraping
    
    #with selected vendors, initialize crawling
    asyncio.run(crawler.init_crawler(["supurge"],["teknosa","vatan"]))


main()