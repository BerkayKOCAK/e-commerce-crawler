from bs4 import BeautifulSoup
import re
import xml.etree.ElementTree as XML_operations
from src import scrape_elements, request_lib



def sitemap_scrape(sitemap):
    #scrape given html content for product links, get all products
    #then return sitemap_parse_XML(scraped_sitemap_xml):
    print("sitemap address "+str(sitemap))
    return 0



def sitemap_parse_XML(sitemap_content):
    #parse the xml
    
    print("sitemap XML ")
    return 0



def product_search(product,sitemap_XML):
    """
    Searches corresponding product in the given XML content.\n
    It simply checks if XML object.text has product name as substring.\n
    Returns searched products as list array.\n
    product = Product name\n
    sitemap_XML = XML content
    """
    productFound = []
    if sitemap_XML:
       
        root = XML_operations.fromstring(sitemap_XML) 
        print("searching "+product+ " in sitemap XML ")
        #TODO - linear search atm. might improve
        for child in root.iter():
            if product in child.text:
                productFound.append(child.text)
    return productFound



def sub_page_URL_generator(vendor,page_URL,pageCount):
    """
    pageCount = Page number\n
    vendor = Vendor name\n
    page_URL = URL of the page
    """
    search_query = "?"+scrape_elements.websites[vendor]['page-query']
    constructed = page_URL + search_query + "=" + str(pageCount)
    #print(" search_query == " +constructed)
    return constructed



"""
Binary search
        Time complexity is O(log N) for both rec and iterative.
        The major difference between the iterative and recursive version of Binary Search 
        is that the recursive version has a *space complexity* of O(log N) 
        while the iterative version has a space complexity of O(1). 
        Hence, even though recursive version may be easy to implement, 
        the iterative version is efficient.
"""
async def find_last_page(vendor,page_URL):
    
    """
        Looks for last page with product listing.\n
        Retrieves pages that algorithm indicates.Then checks if that content has product listing in it.\n
        Active algorithm : Binary Search.\n
        To scrape content uses beautiful soup 4.\n
        vendor = Vendor name\n
        page_URL = URL of the page
    """

    back = 0
    front = 10
    middle = 5
    subPage = sub_page_URL_generator(vendor,page_URL,front)

    while True:

        middle = (back + front)//2
        subPage = sub_page_URL_generator(vendor,page_URL,front)
        scrapable = await page_has_scrape(vendor,subPage)
        if(scrapable):
            back = front
            front = (front * 2) + back

        else:
            subPage = sub_page_URL_generator(vendor,page_URL,middle)
            scrapable = await page_has_scrape(vendor,subPage)
            if (scrapable):
                back = middle
            else:
                front = middle
        
        if (middle + 1) == front:
            break
    return middle



async def page_has_scrape(vendor,page_URL):

    content = await request_lib.GET_request_async(page_URL)
    soup = BeautifulSoup(content, "html.parser")
    website = scrape_elements.websites[vendor]

    if website["product-scope"]["name"]:
        regex_class_name = re.compile(website["product-scope"]["name"])
    else:
        regex_class_name = ''
    
    productElements = soup.find_all(website["product-scope"]["element"], class_= regex_class_name )
    
    if (productElements):
        return True
    else:
        return False