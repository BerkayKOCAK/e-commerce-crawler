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
from src import crawler, utils, scraper
from pprint import pprint

from PyInquirer import style_from_dict, Token, prompt, Separator
from pyfiglet import Figlet
from termcolor import colored

style1 = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})

style2 = style_from_dict({
    Token.Separator: '#33FFEC',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#33FFEC',  # default
    Token.Pointer: '#AF601A bold',
    Token.Instruction: '#EC7063',  # defaults
    Token.Answer: '#AF601A bold',
    Token.Question: '#EC7063',
})


style3 = style_from_dict({
    Token.Separator: '#FDDB5F',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#DEFD5F',  # default
    Token.Pointer: '#AF601A bold',
    Token.Instruction: '#83FD5F',  # defaults
    Token.Answer: '#DEFD5F bold',
    Token.Question: '#FDDB5F',
})

templateCrawlingSelection = [
    {
        'type': 'checkbox',
        'message': 'Choose vendors for crawling',
        'name': 'crawlingVendors',
        'choices': [
            Separator(' = Crawling Vendors = ')
        ],
        'validate': lambda answer: 'You must choose at least one topping.' \
            if len(answer) == 0 else True
    },
    {
        'type': 'confirm',
        'message': 'Do you want to use same vendors for scraping also ?',
        'name': 'sameVendors',
        'default': True,
    },
]

templateScrapingSelection = [
    
    {
        'type': 'checkbox',
        'message': 'Choose vendors for scraping',
        'name': 'scrapingVendors',
        'choices': [
            Separator(' = Scraping Vendors = ')
           
        ],
        'validate': lambda answer: 'You must choose at least one topping.' \
            if len(answer) == 0 else True
    },
]

templateProductSelection = [
    
    {
        'type': 'checkbox',
        'message': 'Choose vendors for scraping',
        'name': 'scrapingProducts',
        'choices': [
            Separator(' = Scraping Vendors = ')
           
        ],
        'validate': lambda answer: 'You must choose at least one topping.' \
            if len(answer) == 0 else True
    },
]

templateProductInput = [
    
    {
        'type': 'input',
        'message': 'Enter some products to crawl in web pages (put comma between multiple products and dont use spaces): ',
        'name': 'products',
        'validate': lambda answer: 'You must choose at least one topping.' \
            if len(answer) == 0 else True
    },
]



def main():
    
    f = Figlet(font='cyberlarge')
    print(f.renderText(' - CRAWLER - '))
    print(f.renderText(' * By Berkay * '))

    utils.instructions()

    #TODO - ask user if it wants to scrape also

    crawlingVendorSelection = utils.menu_add_vendors(templateCrawlingSelection)
    scrapingVendorSelection = utils.menu_add_vendors(templateScrapingSelection)
    crawlingVendors = prompt(crawlingVendorSelection, style=style1)
    
    if(len(crawlingVendors['crawlingVendors']) != 0):
        
        if (crawlingVendors['sameVendors']):
            scrapingVendors = crawlingVendors['crawlingVendors']
        else:
            scrapingVendors = prompt(scrapingVendorSelection, style=style1)
            scrapingVendors = scrapingVendors["scrapingVendors"]
        
        print("Selected Vendors for Crawling: " + str(crawlingVendors['crawlingVendors']))
        print("Selected Vendors for Scraping: " + str(scrapingVendors))
    else: exit(0)
    
    asyncio.run(utils.timeout(1))

    if (utils.file_integrity()):

        if ("None" in crawlingVendors['crawlingVendors'] and "None" in scrapingVendors ):
            print(colored('No vendor selected for both operations, no need to stay in run-time then.', 'red'))
            exit(0)

        elif "None" in crawlingVendors['crawlingVendors']:
            print(colored('Only scraper will operate', 'red'))
            utils.vendor_folder_mapping()
            utils.product_folder_mapping(scrapingVendors)
            scrapingProductSelection = utils.menu_add_products(templateProductSelection)
            scrapingProducts = prompt(scrapingProductSelection, style=style2)
            asyncio.run(scraper.scraper_init(scrapingVendors,scrapingProducts['scrapingProducts']))
        
        elif "None" in scrapingVendors:
            print(colored('Only crawler will operate', 'red'))
            crawlingProducts = prompt(templateProductInput, style=style3)
            crawlingProductsArray = str(crawlingProducts).split(",")
            asyncio.run(crawler.init_crawler(crawlingProductsArray,crawlingVendors['crawlingVendors']))
            
        else:
            utils.vendor_folder_mapping()
            utils.product_folder_mapping(scrapingVendors)
            crawlingProducts = prompt(templateProductInput, style=style2)
            scrapingProductSelection = utils.menu_add_products(templateProductSelection)
            scrapingProducts = prompt(scrapingProductSelection, style=style2)
            asyncio.run(crawler.init_crawler(crawlingProducts,crawlingVendors['crawlingVendors']))
            asyncio.run(scraper.scraper_init(scrapingVendors,scrapingProducts['scrapingProducts']))

    else:
        print(colored('Could not find scraper.py and csv_lib.py. Thus, only crawler will operate', 'red'))
        crawlingProducts = prompt(templateProductInput, style=style3)
        crawlingProductsArray = str(crawlingProducts).split(",")
        asyncio.run(crawler.init_crawler(crawlingProductsArray,crawlingVendors['crawlingVendors']))


    #ask for words to exclude at search
    #ask for products support adjectives, Ex supurge -> elektirikli == search(elektrikli and supurge)
    
main()