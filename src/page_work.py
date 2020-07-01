from bs4 import BeautifulSoup
import re
import xml.etree.ElementTree as XML_operations
from src import scrape_elements, request_lib
from urllib.parse import unquote
from xml.dom import minidom

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



def product_search(product,sitemapList,excludedProductNames):
    
    productFound = []
    productWords_Arr = []
    #print(excludedProductNames)
    if("-" in product): productWords_Arr = product.lower().split("-")   
    else: productWords_Arr.append(product.lower())

    if sitemapList:
        
        for link in sitemapList:
            
            if (any(wordEx in link for wordEx in excludedProductNames) == False):
                
                if (len(productWords_Arr) > 0 ):
                    
                    count = 0
                    for word in productWords_Arr:
                        
                        if word in link.lower():
                            count += 1
                    if count != len(productWords_Arr): pass#print("False")
                    else: productFound.append(link)
                    
                elif (product in link) and (link not in productFound):
                    productFound.append(link)
            else: continue# Excluded Word fount

        if len(productFound) == 0:
                
                #convert special letters like ğ-ö to g-o
                temp = product
                product = product.lower()
                product = product.translate(scrape_elements.special_char_map)
                print(" <<< Reconstructed the product string as = "+ product +" >>>")
                if temp == product:
                    print(" <<< Reconstructed the product string previous one was same :( >>>")
                    return productFound
                productFound = product_search(product,sitemapList,excludedProductNames)
    return productFound



def product_search_xml(product,sitemap_XML,excludedProductNames):
    """
    Searches corresponding product in the given XML content.\n
    It simply checks if XML object.text has product name as substring.\n
    Returns searched products as list array.\n
    product = Product name\n
    sitemap_XML = XML content
    """
    productFound = []
    productWords_Arr = []
    if("-" in product):
        productWords_Arr = product.split("-")


    if sitemap_XML:
 
        xmlstr = minidom.parseString(sitemap_XML).toprettyxml(indent="    ",newl="\n", encoding="UTF-8")
        root = XML_operations.fromstring(xmlstr)
        print("searching "+product+ " in sitemap XML ")

        try:

            for child in root.iter():
                if(child.text != None):
                    text = unquote(child.text, errors='strict')
                    
                    if (any(wordEx in text for wordEx in excludedProductNames) == False):
                        #print("for text "+text+" looks ex : "+str(any(wordEx in text for wordEx in productWords_Arr)))
                        if (len(productWords_Arr) > 0 ):
                            count = 0
                            for word in productWords_Arr:
                                if word in text:
                                    count += 1
                            if count != len(productWords_Arr): pass#print("False")
                            else: productFound.append(text)     
                        elif product in text:
                            productFound.append(text)

                    else:continue# Excluded Word found
                else:continue
                    #print("Defect xml node found!")
                    
                    
        except Exception as e:
            print("ERROR ! PRODUCT SEARCH IN XML \nMESSAGE : "+str(e))
            
        #There might be special chracters for user's query. For example, süpürge --> supurge
        if len(productFound) == 0:
            
            #convert special letters like ğ-ö to g-o
            temp = product
            product = product.translate(scrape_elements.special_char_map)
            print(" <<< Reconstructed the product string as = "+ product +" >>>")
            if temp == product:
                print(" <<< Reconstructed the product string but found none again :( >>>")
                return productFound
            productFound = product_search_xml(product,sitemap_XML,excludedProductNames)

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
    try:
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
    except Exception as e:
        print("\n0000 ERROR IN page_has_scrape 000 \nMESSAGE : "+ str(e))
        return False