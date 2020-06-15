from src import request_lib, scrape_elements, utilities, page_work
import os
import asyncio



async def init_crawler(productList,vendorList):
    #check if vendor folders created, if not create

    #string resulution for product name
    
    #queue each vendor as linear task
        print(" VENDOR QUEUE STARTS")
        await vendor_queue(productList,vendorList)

#For each vendor task (asynch) [vendor_queue]
    #queue each product as parallel tasks [product_queue] with parallel sub-tasks for that products each page (asynch)
        #   Parallel product tasks must find desired product in vendors sitemap and retrieve page links for that product (asynch)
        #   then on each page connection use GET method to retrieve content and then write that content to a file (synch)

async def vendor_queue(productList,vendorList):
    vendor_tasks = []
    
    try:
        for vendor in vendorList:
            print("Task Created For Vendor : "+vendor)
            vendor_tasks.append(asyncio.ensure_future(product_queue(productList,vendor)))
    
        while vendor_tasks:
            print(" **** Vendor Tasks are started **** ")
            done, pending = await asyncio.wait(vendor_tasks)
            #print(done)
            #print(pending)
            vendor_tasks[:] = pending
        print("**** Vendor Tasks are ended **** ")
    except Exception as e:
        print(" @@@@ ERROR IN VENDOR QUEUE  @@@@ \n MESSAGE : "+ str(e))



"""
def vendor_queue_blocking(productList,vendorList):
    
    for vendor in vendorList:
        print("VENDOR : "+vendor)
        product_queue(productList,vendor)
"""



async def product_queue(productList,vendor):
    product_tasks = []
    #url = scrape_elements.websites[vendor]["url"]
    nonXML = scrape_elements.websites[vendor]["non-xml-map"]
    sitemap = scrape_elements.websites[vendor]["sitemap"]
    sitemap_category = scrape_elements.websites[vendor]["sitemap-category"]
    
    try:
        if (nonXML):
            sitemap_XML = page_work.sitemap_scrape(sitemap)
        else:
            print("sitemap_category address: "+sitemap_category)
            sitemap_XML = request_lib.GET_request(sitemap_category)
            
        for product in productList:
            print("Task Created For Product : "+product)
            page_list = page_work.product_search(product,sitemap_XML)
            product_tasks.append(asyncio.ensure_future(page_queue(vendor,product,page_list)))
    
        while product_tasks:
            print(" **** Product Tasks are started **** ")
            done, pending = await asyncio.wait(product_tasks)
            #print(done)
            #print(pending)
            product_tasks[:] = pending
        print("**** Product Tasks are ended **** ")
    except Exception as e:
        print(" @@@@ ERROR IN PRODUCT QUEUE  @@@@ \n MESSAGE : "+ str(e))



async def page_queue(vendor,product,page_list):
    print(vendor+" - page queue, product : "+product)
    # for each page in page_list, 
    #   write content to a file as html.



def url_GET_crawler(vendor):
    url = scrape_elements.websites[vendor]["url"]
    request_lib.GET_request(url)
