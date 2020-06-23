from src import request_lib, scrape_elements, utils, page_work
import os
import asyncio



async def init_crawler(productList,vendorList):

    #string resulution for excluded product names

    print(" VENDOR QUEUE STARTS")
    await vendor_queue(productList,vendorList)


#For each vendor task (asynch) [vendor_queue]
    #queue each product as parallel tasks [product_queue] with parallel sub-tasks for that products each page (asynch)
        #   Parallel product tasks must find desired product in vendors sitemap and retrieve page links for that product (asynch)
        #   then on each page connection use GET method to retrieve content and then write that content to a file (synch)

async def vendor_queue(productList,vendorList):
    """
    Queues vendor jobs as unique tasks at vendorList.
    \nFor each vendor in vendor list; \n\t call product_queue as task

    productList = List of products, which are given by user.
    vendorList  = List of vendor, which are choosen by user.
    """
    vendorTasks = []
    
    try:

        for vendor in vendorList:
            nonXML = scrape_elements.websites[vendor]["non-xml-map"]
            sitemap = scrape_elements.websites[vendor]["sitemap"]                   #URL of page oriented sitemap.
            sitemapCategory = scrape_elements.websites[vendor]["sitemap-category"]  #URL of xml oriented sitemap.
            utils.create_vendor_folder(vendor)

            if (nonXML):
                sitemapContent = await request_lib.GET_request_async(sitemap)
                sitemapList = page_work.sitemap_scrape(vendor,sitemapContent)
                print("Task Created For Vendor : "+vendor+ " with non-XML sitemap")
                vendorTasks.append(asyncio.ensure_future(product_queue(productList,vendor,sitemapList,False)))

            else:
                print("sitemapCategory address: "+sitemapCategory)
                #TODO - make it a stream call. Regular get might stuck for large xmls
                sitemap_XML = request_lib.GET_request(sitemapCategory)
                print("Task Created For Vendor : "+vendor+" with regular sitemap")
                vendorTasks.append(asyncio.ensure_future(product_queue(productList,vendor,sitemap_XML,True)))

        while vendorTasks:
            print(" **** Vendor Tasks are started **** ")
            done, pending = await asyncio.wait(vendorTasks)
            #print(done)
            #print(pending)
            vendorTasks[:] = pending
        print("**** Vendor Tasks are ended **** ")
    except Exception as e:
        print(" @@@@ ERROR IN VENDOR QUEUE  @@@@ \n MESSAGE : "+ str(e))



"""
def vendor_queue_blocking(productList,vendorList):
    
    for vendor in vendorList:
        print("VENDOR : "+vendor)
        product_queue(productList,vendor)
"""



async def product_queue(productList,vendor,sitemapHolder,isXml):
    """
    Queues each product in productList as tasks.
    \nFor each product in productList;\n\t call page_queue to work on pages of the product\n
    productList =  List array of products\n
    Vendor = Vendor name\n
    sitemap_XML = Sitemap for vendor.(In xml form)
    """
    productTasks = []

    try:
    
        
        for product in productList:
            print("Task Created For Product : "+product)
            if isXml:
                pageList = page_work.product_search_xml(product,sitemapHolder)
            else:
                pageList = page_work.product_search(product,sitemapHolder)
            
            print("product :"+ product +" pageList : "+str(pageList))
            productTasks.append(asyncio.ensure_future(page_queue(vendor,product,pageList)))
    
        while productTasks:
            print(" **** Product Tasks are started for : "+vendor+" **** ")
            done, pending = await asyncio.wait(productTasks)
            #print(done)
            #print(pending)
            productTasks[:] = pending
        print("**** Product Tasks are ended for "+vendor+" **** ")
    except Exception as e:
        print(" @@@@ ERROR IN PRODUCT QUEUE  @@@@ \n MESSAGE : "+ str(e))



async def page_queue(vendor,product,pageList):
    """
    Page queuer for products. Queues each related page dependent jobs to product. 
    \nFor each page in page list; \n\tcall sub_page_worker in a task to write content of the web pages.\n
    Vendor = Vendor name\n
    product = Product name\n
    pageList = List array of pages
    """
    subPageTasks = []
    print(vendor+" - page queue, product : "+product)
    productFolder = utils.create_product_folder(vendor,product)
    try:
 
        for page in pageList:
            print("PAGE == "+page)
            
            content = await request_lib.GET_request_async(page)
            
            if(content):
                #there are discount pages with the name of the product in it but in general
                #those pages dont have a grid like product listings and/or sub pages.
                #so we need to prune those before working on them!
               
                isScrapable = await page_work.page_has_scrape(vendor,content)
                if( isScrapable ):
                    pageName = utils.url_name_strip(page)
                    utils.html_writer(productFolder,pageName,content)
                    subPageTasks.append(asyncio.ensure_future(sub_page_worker(vendor,product,page,productFolder)))
        
        while subPageTasks:
            print(" **** paging Tasks are started for product : "+product+" **** ")
            done, pending = await asyncio.wait(subPageTasks)
            #print(done)
            #print(pending)
            subPageTasks[:] = pending
        print("**** paging Task is ended for product : "+product+" **** ")
            
    except Exception as e:
        print(" === ERROR IN PAGE QUEUE  === \n MESSAGE : "+ str(e))



async def sub_page_worker(vendor,product,page,productFolder):
    """
    Looks for given page's sub pages.Then for each; retrieves content and writes it as html.\n
    Vendor = Vendor name\n
    product = Product name\n
    page = URL of the page\n
    productFolder = Path of the product folder\n
    """
    print("SUB-PAGE Task for product : "+product+" - sub page queue, page : "+page)
    
    pageCount = 0
    lastPageNum = await page_work.find_last_page(vendor,page)
    print("last page num  for "+ page +" == "+str(lastPageNum))
    while pageCount < lastPageNum:
        subPage = page_work.sub_page_URL_generator(vendor,page,pageCount)
        subPageName = utils.url_name_strip(subPage) + str(pageCount)
        content = await request_lib.GET_request_async(subPage)
        pageCount = pageCount + 1
        utils.html_writer(productFolder,subPageName,content)
        print("HTML PAGE WRITTEN : "+ subPageName)
    print("**** SUB-PAGE Task is ended for : "+page+" **** ")
