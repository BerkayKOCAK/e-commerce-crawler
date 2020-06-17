from src import request_lib, scrape_elements, utils, page_work
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
            nonXML = scrape_elements.websites[vendor]["non-xml-map"]
            sitemap = scrape_elements.websites[vendor]["sitemap"]
            sitemap_category = scrape_elements.websites[vendor]["sitemap-category"]
            utils.create_vendor_folder(vendor)

            if (nonXML):
                sitemap_XML = page_work.sitemap_scrape(sitemap)
                print("Task Created For Vendor : "+vendor+ " with non-XML sitemap")
                vendor_tasks.append(asyncio.ensure_future(product_queue(productList,vendor,sitemap_XML)))

            else:
                print("sitemap_category address: "+sitemap_category)
                #TODO - make it a stream call. Regular get might stuck for large xmls
                #sitemap_XML = request_lib.GET_request_stream(sitemap_category)
                sitemap_XML = request_lib.GET_request(sitemap_category)
                print("Task Created For Vendor : "+vendor+" with regular sitemap")
                vendor_tasks.append(asyncio.ensure_future(product_queue(productList,vendor,sitemap_XML)))

            
    
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



async def product_queue(productList,vendor,sitemap_XML):
    product_tasks = []

    try:
       
        for product in productList:
            print("Task Created For Product : "+product)
            page_list = page_work.product_search(product,sitemap_XML)
            print("product :"+ product +" page_list : "+str(page_list))
            product_tasks.append(asyncio.ensure_future(page_queue(vendor,product,page_list)))
    
        while product_tasks:
            print(" **** Product Tasks are started for : "+vendor+" **** ")
            done, pending = await asyncio.wait(product_tasks)
            #print(done)
            #print(pending)
            product_tasks[:] = pending
        print("**** Product Tasks are ended for "+vendor+" **** ")
    except Exception as e:
        print(" @@@@ ERROR IN PRODUCT QUEUE  @@@@ \n MESSAGE : "+ str(e))


async def page_queue(vendor,product,page_list):
    
    print(vendor+" - page queue, product : "+product)
    product_folder = utils.create_product_folder(vendor,product)

    for page in page_list:
        print("PAGE == "+page)
        #request = await event_loop.run_in_executor(None, request_lib.GET_request_async, page)
        content = await request_lib.GET_request_async(page)
        if(content != None):
            page_name = utils.url_name_strip(page)
            utils.html_writer(product_folder,page_name,content)
         
    #for each page in page_list,
    #   write content to a file as html.
    #   call sub_page_queue

async def sub_page_queue(vendor,product,page_name):
    
    print("product : "+product+" - sub page queue, page : "+page_name)
    # for each page in page_list, 
    #   write content to a file as html.


def url_GET_crawler(vendor):
    url = scrape_elements.websites[vendor]["url"]
    request_lib.GET_request(url)
