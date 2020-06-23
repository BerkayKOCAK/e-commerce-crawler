from bs4 import BeautifulSoup
import re
import xml.etree.ElementTree as XML_operations
from src import scrape_elements, request_lib
from urllib.parse import unquote
from xml.dom import minidom

#TODO - you need to manage slashes(/) on urls, there are some cases like https://// and zzz.com///product/...
def sitemap_scrape(vendor,sitemapContent):

    soup = BeautifulSoup(sitemapContent, "html.parser")
    website = scrape_elements.websites[vendor]
    allLinks = soup.find_all("a",href=True)
    sitemapLinks = []

    for link in allLinks:
        
        if ( "http" or "https") in link['href']: sitemapLinks.append(link['href'])
        
        elif "www." in link['href']:
            slashNumber = 0
            start = link['href'].find("/")
            for char in link['href']:
                if( char == "/"): slashNumber += 1
                if( char == "w"): break

            if slashNumber == 2: realLink = "https:"+link['href'][start:]
            else: realLink = "https://"+link['href'][start:]
        
            sitemapLinks.append(realLink)
        
        elif(website["url"] not in link) and ( len(link['href']) > 2 ):
            linkText = link['href'].replace("/","")
            realLink = website["url"] + linkText
            sitemapLinks.append(realLink)

    return sitemapLinks



def product_search(product,sitemapList):
    
    productFound = []
    if sitemapList:
        for link in sitemapList:
            if (product in link) and (link not in productFound):
                productFound.append(link)

        if len(productFound) == 0:
                
                #convert special letters like ğ-ö to g-o
                special_char_map = {ord('ä'):'a', ord('ü'):'u', ord('ö'):'o', ord('ş'):'s', ord('ç'):'c',ord('ğ'):'g'}
                temp = product
                product = product.translate(special_char_map)
                print(" <<< Reconstructed the product string as = "+ product +" >>>")
                if temp == product:
                    print(" <<< Reconstructed the product string previous one was same :( >>>")
                    return productFound
                productFound = product_search(product,sitemapList)
    return productFound



def product_search_xml(product,sitemap_XML):
    """
    Searches corresponding product in the given XML content.\n
    It simply checks if XML object.text has product name as substring.\n
    Returns searched products as list array.\n
    product = Product name\n
    sitemap_XML = XML content
    """
    productFound = []

    if sitemap_XML:
 
        xmlstr = minidom.parseString(sitemap_XML).toprettyxml(indent="    ",newl="\n", encoding="UTF-8")
        root = XML_operations.fromstring(xmlstr)
        print("searching "+product+ " in sitemap XML ")
        #print(root.findall("*"))

        try:

            for child in root.iter():
                if(child.text != None):
                    text = unquote(child.text, errors='strict')
                    #print(child.tag, child.attrib)
                    if product in text:
                        productFound.append(text)
                else:
                    #print("Defect xml node found!")
                    pass
                    
        except Exception as e:
            print("ERROR "+str(e))
            
        #There might be special chracters for user's query. For example, süpürge --> supurge
        if len(productFound) == 0:
            #convert special letters like ğ-ö to g-o
            special_char_map = {ord('ä'):'a', ord('ü'):'u', ord('ö'):'o', ord('ş'):'s', ord('ç'):'c',ord('ğ'):'g'}
            temp = product
            product = product.translate(special_char_map)
            print(" <<< Reconstructed the product string as = "+ product +" >>>")
            if temp == product:
                print(" <<< Reconstructed the product string but found none again :( >>>")
                return productFound
            productFound = product_search_xml(product,sitemap_XML)

    return productFound



def iterable(obj):
    """Check if object is iterable"""
    try: iter(obj) 
    except Exception: return False
    else: return True
       


def sub_page_URL_generator(vendor,page_URL,pageCount):
    """
    pageCount = Page number\n
    vendor = Vendor name\n
    page_URL = URL of the page
    """
    search_query = "?"+scrape_elements.websites[vendor]['page-query']
    constructed = page_URL + search_query + "=" + str(pageCount)
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
    """
    Check if the page has scrapable product elements.\n
    Uses Beautiful Soup, looks up the product listing element which is predefined at scrape_elements.py\n
    vendor = Vendor name\n
    page_URL = URL of the page to check\n
    """
    content = await request_lib.GET_request_async(vendor,page_URL)

    if(content != None):
        soup = BeautifulSoup(content, "html.parser")
        website = scrape_elements.websites[vendor]

        if website["product-scope"]["name"]:
            regex_class_name = re.compile(website["product-scope"]["name"])
        else:
            regex_class_name = ''
        
        productElements = soup.find_all(website["product-scope"]["element"], class_= regex_class_name )
        
        if (productElements):
            #print(" 000> Page  is scrapable.")
            return True
        else:
            #print(" +++> Page  is not scrapable because there is no product scope in its dom elements.")
            #print("Product scope can be find at corresponding vendor's scrape_elements.py mapping. ")
            return False
    else:
        #print(" +++> Page  is not scrapable because there is no content !")
        return False