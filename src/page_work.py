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
    #return searched products as list array
    product_found = []
    if sitemap_XML:
       
        root = XML_operations.fromstring(sitemap_XML) 
        print("searching "+product+ " in sitemap XML ")
        #TODO - linear search atm. might improve
        for child in root.iter():
            if product in child.text:
                product_found.append(child.text)
    return product_found



def sub_page_URL_generator(vendor,page_url,page_count):
    search_query = "?"+scrape_elements.websites[vendor]['page-query']
    constructed = page_url + search_query + "=" + str(page_count)
    #print(" search_query == " +constructed)
    return constructed



async def find_last_page(vendor,page_url):
    #a simple scrape with bs4
    """
        Time complexity is O(log N) for both rec and iterative.
        The major difference between the iterative and recursive version of Binary Search 
        is that the recursive version has a *space complexity* of O(log N) 
        while the iterative version has a space complexity of O(1). 
        Hence, even though recursive version may be easy to implement, 
        the iterative version is efficient.

    """

    back = 0
    front = 10
    middle = 5
    sub_page = sub_page_URL_generator(vendor,page_url,front)

    while True:

        middle = (back + front)//2
        sub_page = sub_page_URL_generator(vendor,page_url,front)
        scrapable = await page_has_scrape(vendor,sub_page)
        if(scrapable):
            back = front
            front = (front * 2) + back

        else:
            sub_page = sub_page_URL_generator(vendor,page_url,middle)
            scrapable = await page_has_scrape(vendor,sub_page)
            if (scrapable):
                back = middle
            else:
                front = middle
        
        if (middle + 1) == front:
            break
    return middle



async def page_has_scrape(vendor,page_url):

    content = await request_lib.GET_request_async(page_url)
    soup = BeautifulSoup(content, "html.parser")
    website = scrape_elements.websites[vendor]

    if website["product-scope"]["name"]:
        regex_class_name = re.compile(website["product-scope"]["name"])
    else:
        regex_class_name = ''
    
    product_elements = soup.find_all(website["product-scope"]["element"], class_= regex_class_name )
    
    if (product_elements):
        return True
    else:
        return False