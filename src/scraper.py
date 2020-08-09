
"""
   Main scraping script.

   Includes:
    * scraper_init
    * scraper_queue
    * product_scraper
"""

from bs4 import BeautifulSoup
import re
from src import utils, scrape_elements, csv_lib
from pathlib import Path
import os
import asyncio
import logging


async def scraper_init (selected_vendors,selected_products):
    """ Initializer for scraping operation """
    if ("None" in selected_vendors) or ("None" in selected_products): 
        logging.error("None selected at scraper selection for current assets!")
        return None
    else:
        logging.info("SCARAPER STARTS : ")
        for vendor in selected_vendors:
            logging.info("Vendor : "+vendor)
            await scraper_queue(vendor,selected_products)



async def scraper_queue(vendor,selected_products):
    """ Queues all the scraping tasks to work in parallel.
        Simply appends tasks to a task array and when a task returns, removes it from the arrays .
    """
    count = 1
    tasks = []
    try:    
        for productName in selected_products: 
            page = 1
            
            fileListToOpen =  scrape_elements.products.get(vendor)['products'].get(productName)
           
            if fileListToOpen != None:
                for fileToOpen in fileListToOpen: 
                    if os.path.isfile(fileToOpen):
                        if(scrape_elements.websites.get(str(vendor)) != None):
                            with open(fileToOpen, encoding='utf8') as infile:
                                soup = BeautifulSoup(infile, "html.parser")

                                logging.info("CREATING WORKER_"+str(count)+" FOR VENDOR : "+ str(vendor)+" AND PRODUCT : "+productName + " FOR PAGE : "+str(fileToOpen))
                                tasks.append(asyncio.ensure_future(product_scraper(vendor+"_"+str(count), soup, scrape_elements.websites.get(vendor), productName )))
                                count = count + 1  
                                page = page + 1    
                        else:
                            logging.error("Cannot Found Vendor "+ vendor +" in mapping !")
                            pass
                    else:
                        logging.error("Path "+fileToOpen+" indicates no file !")
            else:
                logging.error("On Vendor - "+ vendor +" - No File Found For Product : "+productName)
                #Unnecessary info, u might prune it.           
                             
                
        #TODO - For bigger data divide task management to batches and limit the parallelized tasks to 10. 
        while tasks:
            logging.info(" **** Tasks are started **** ")
            done, pending = await asyncio.wait(tasks)
            #logging.info(done)
            #logging.info(pending)
            tasks[:] = pending
        logging.info("**** Tasks are ended **** ")

        #for task in tasks:
        #    await task

    except Exception as e:
        logging.critical(" @@@@ ERROR IN QUEUE  @@@@ \n MESSAGE : "+ str(e))



async def product_scraper(taskName,soup,website,product):
    """ 
        This is where the magic happens.\n
        It gets dom elements in soup and then finds the desired ones via beautifulsoup\n
        To operate, it needs to know which elements will be scraped thus the website item must include structure similiar to one in scrape_elements.website\n
        #Same applies for the product.
    """
    #logging.info("VENDOR : "+website.get("name")+" PRODUCT : "+product)
    scrape_array = []
    
    try:

        
        if website["product-scope"]["name"]:
            regex_class_name = re.compile(website["product-scope"]["name"])
        else:
            regex_class_name = ''
        if website["child-element"]['title_regex']:
            regex_title = re.compile(website["child-element"]['title_regex'])
            
        else:
            regex_title = ''
        if website["child-element"]['price_regex']:
            regex_price = re.compile(website["child-element"]['price_regex'])
        else:
           regex_price = ''
        
        product_elements = soup.find_all(website["product-scope"]["element"], class_= regex_class_name )
        for child in product_elements:
            
            child_title_list = child.find_all(website["child-element"]["title"], {"class" : regex_title})
            child_price = child.find(website["child-element"]["price"], {"class" : regex_price})
            child_old_price = child.find(website["child-element"]["old_price"], {"class" : regex_price})
            scrape_item = {}

            if len(child_title_list) > 1:
                child_title = ""
                for substr in child_title_list:
                    child_title = child_title +" "+ substr.text.strip()
            else:
                child_title = child_title_list[0]
           
            #strip the text from dom element
            # headers = ['productName', 'price(TL)',"old_price(TL)"]
           
            if isinstance(child_title, str):
                #logging.info(taskName+" productName : "+ child_title)
                scrape_item["productName"] = child_title
            else:
                #logging.info(taskName+" productName : "+ child_title.text.strip())
                scrape_item["productName"] = child_title.text.strip()
            
            if child_price:
                #logging.info( taskName+ " PRICE : "+ child_price.text.strip())
                scrape_item["price(TL)"] = child_price.text.strip()
            
            if child_old_price:
                #logging.info(taskName+ " OLD PRICE : "+ child_old_price.text.strip())
                scrape_item["old_price(TL)"] = child_old_price.text.strip()
            
            scrape_array.append(scrape_item)
        csv_lib.write_csv(website.get("name"),product,scrape_array)
        #TODO - append if already created
    except Exception as identifier:
        logging.critical("ERROR IN" + taskName +" PRODUCT-SCRAPER "+ str(identifier))

