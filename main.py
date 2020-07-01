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

#Scraper = sc
#Crawler = cw

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

templateScList = {
        'type': 'list',
        'message': 'What do you want scraper to work with ? \nWith new assets after the crawling operation, with currently available assets or both... ',
        'name': 'operationList',
        'choices': ["New Assets","Current Assets","Both"]
    }

templateScQuestion = {
        'type': 'confirm',
        'message': 'Do yo want to include scraping operations for files?',
        'name': 'scrapingOpt',
        'default': True,
    }


templateSameVendorQuestion = {
        'type': 'confirm',
        'message': 'Do you want to use same vendors at scraping operation for current files ? ',
        'name': 'sameVendors',
        'default': True,
    }

templateCwSelection = [
    {
        'type': 'checkbox',
        'message': 'Choose vendors for crawling',
        'name': 'cw_vendors',
        'choices': [
            Separator(' = Available Crawling Vendors = ')
        ],
        'validate': lambda answer: 'You must choose at least one topping.' \
            if len(answer) == 0 else True
    }
]

templateScSelection = [
    
    {
        'type': 'checkbox',
        'message': 'Choose vendors for scraping',
        'name': 'sc_vendors',
        'choices': [
            Separator(' = Available Scraping Vendors = ')
           
        ],
        'validate': lambda answer: 'You must choose at least one topping.' \
            if len(answer) == 0 else True
    },
]

templateProductSelection = [
    
    {
        'type': 'checkbox',
        'message': 'Choose products for scraping from assets.',
        'name': 'sc_selectedProducts',
        'choices': [
            Separator(' = Available Scraping Products = ')
           
        ],
        'validate': lambda answer: 'You must choose at least one topping.' \
            if len(answer) == 0 else True
    },
]

templateProductInput = [
    
    {
        'type': 'input',
        'message':  """
                    Enter some products to crawl in web pages
                    \n*If name of the product consists of multiple words, use \"-\" symbol between words as seperator
                    \n*Put comma between multiple products and dont use spaces: """
                    ,
        'name': 'products',
        'validate': lambda answer: 'You must choose at least one topping.' \
            if len(answer) == 0 else True
    },
]

templateProductExclude = [
    
    {
        'type': 'input',
        'message': "Enter words to exclude. Put comma between multiple words\n* Words you enter must be case and special character sensitive!",
        'name': 'excludedProducts'
    },
]


def main():
    
    f = Figlet(font='cyberlarge')
    print(f.renderText(' - CRAWLER - '))
    print(f.renderText(' * By Berkay * '))

    utils.instructions()
    cw_vendorSelection = utils.menu_add_vendors(templateCwSelection)
    sc_vendorSelection = utils.menu_add_vendors(templateScSelection)
    sc_vendors = []
    sc_productSelection = []
    
    try:
        
        useScraper = prompt(templateScQuestion, style=style1)
       
        if (useScraper["scrapingOpt"]):
            sc_list = prompt(templateScList, style=style1)
            cw_vendors = prompt(cw_vendorSelection, style=style1)
            if(len(cw_vendors['cw_vendors']) != 0):
                
                tempVendors = cw_vendors['cw_vendors']
                templateSameVendorQuestion['message'] = templateSameVendorQuestion['message'] + " --> "+str(tempVendors)
                
                if(("Both") or ("Current Assets") in sc_list['operationList']):
                    sameVendors = prompt(templateSameVendorQuestion, style = style1)
                    if (sameVendors['sameVendors']):
                        sc_vendors = cw_vendors['cw_vendors']
                    else:
                        sc_vendors = prompt(sc_vendorSelection, style=style1)
                        sc_vendors = sc_vendors["sc_vendors"]
                    print("Selected Vendors for Cw: " + str(cw_vendors['cw_vendors']))
                    print("Selected Vendors for Sc: " + str(sc_vendors))
                else: pass
                
               

            elif (not useScraper["scrapingOpt"]): pass
            else: exit(0)

        else: pass
        
        asyncio.run(utils.timeout(1))

        if (utils.file_integrity() and useScraper["scrapingOpt"]):

            if "Both" in sc_list['operationList']:

                if ("None" in cw_vendors['cw_vendors'] and "None" in sc_vendors ):
                    print(colored('No vendor selected for both operations, no need to stay in run-time then.', 'red'))
                    exit(0)

                elif "None" in cw_vendors['cw_vendors']:
                    
                    print(colored('Only scraper will operate', 'red'))
                    utils.vendor_folder_mapping()
                    utils.product_folder_mapping(sc_vendors)

                    sc_productSelection = utils.menu_add_products(templateProductSelection)
                    sc_selectedProducts = prompt(sc_productSelection, style=style2)

                    asyncio.run(scraper.scraper_init(sc_vendors,sc_selectedProducts['sc_selectedProducts']))
                
                elif "None" in sc_vendors:
                   
                    print(colored('Only crawler will operate', 'red'))
                    cw_selectedProducts = prompt(templateProductInput, style=style3)
                    cw_productsArr = str(cw_selectedProducts).split(",")
                    
                    cw_excludedProducts = prompt(templateProductExclude, style=style1)
                    cw_excludedArr = str(cw_excludedProducts).split(",")
                    
                    asyncio.run(crawler.init_crawler(cw_productsArr,cw_vendors['cw_vendors'],cw_excludedArr))
                    
                else:
                    
                    print(colored('First, scraper will for for current assets,\nThen, crawler will get desired products content\nAt last, scraper will work for new assets', 'red'))
                    utils.vendor_folder_mapping()
                    utils.product_folder_mapping(sc_vendors)

                    cw_selectedProducts = prompt(templateProductInput, style=style2)
                    cw_productsArr = str(cw_selectedProducts["products"]).split(",")
                   
                    cw_excludedProducts = prompt(templateProductExclude, style=style1)
                    cw_excludedArr = str(cw_excludedProducts).split(",")
                    print(cw_productsArr)

                    sc_productSelection = utils.menu_add_products(templateProductSelection)
                    sc_selectedProducts = prompt(sc_productSelection, style=style2)
                    
                    print(colored(' -- Scraper works for current assets -- ', 'cyan'))
                    asyncio.run(utils.timeout(1))
                    asyncio.run(scraper.scraper_init (sc_vendors,sc_selectedProducts['sc_selectedProducts']) )
                    
                    print(colored(' -- Crawler Starts -- ', 'cyan'))
                    asyncio.run(utils.timeout(1))
                    asyncio.run(crawler.init_crawler(cw_productsArr,cw_vendors['cw_vendors'],cw_excludedArr))
                  
                    utils.vendor_folder_mapping()
                    utils.product_folder_mapping(sc_vendors)

                    print(colored(' -- Scraper works for new assets -- ', 'cyan'))
                    sc_productSelection = utils.menu_add_products(templateProductSelection)
                    sc_selectedProducts = prompt(sc_productSelection, style=style2)
                    asyncio.run(utils.timeout(1))
                    asyncio.run(scraper.scraper_init (cw_vendors['cw_vendors'],sc_selectedProducts['sc_selectedProducts']) )

            elif "Current Assets" in sc_list['operationList']:
                    
                    print(colored('Only scraper will operate', 'red'))

                    utils.vendor_folder_mapping()
                    utils.product_folder_mapping(sc_vendors)

                    sc_productSelection = utils.menu_add_products(templateProductSelection)
                    sc_selectedProducts = prompt(sc_productSelection, style=style2)

                    asyncio.run(scraper.scraper_init(sc_vendors,sc_selectedProducts['sc_selectedProducts']))

            else:

               

                print(colored('Scraper will work only for incoming new assets after crawling ends.', 'red'))
                cw_selectedProducts = prompt(templateProductInput, style=style3)
                cw_productsArr = str(cw_selectedProducts["products"]).split(",")
                   
                cw_excludedProducts = prompt(templateProductExclude, style=style1)
                cw_excludedArr = str(cw_excludedProducts).split(",")
                print(cw_productsArr)

                asyncio.run(crawler.init_crawler(cw_productsArr,cw_vendors['cw_vendors'],cw_excludedArr))

                utils.vendor_folder_mapping()
                utils.product_folder_mapping(sc_vendors)
                
                asyncio.run(scraper.scraper_init(cw_vendors['cw_vendors'],cw_productsArr))

        else:
            print(colored('Only crawler will operate', 'red'))

            cw_vendors = prompt(cw_vendorSelection, style=style1)
            cw_selectedProducts = prompt(templateProductInput, style=style3)
            cw_productsArr = str(cw_selectedProducts["products"]).split(",")
            cw_excludedProducts = prompt(templateProductExclude, style=style1)
            cw_excludedArr = str(cw_excludedProducts['excludedProducts']).split(",")
            
            asyncio.run(crawler.init_crawler(cw_productsArr,cw_vendors['cw_vendors'],cw_excludedArr))

    except Exception as identifier:
        print("ERROR IN MAIN : "+str(identifier))
    
main()
exit(0)