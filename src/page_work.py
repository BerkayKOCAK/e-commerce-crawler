
import xml.etree.ElementTree as XML_operations
def sitemap_scrape(sitemap):
    #scrape given html content for product links, get all products
    #then return sitemap_parse_XML(scraped_sitemap_xml):
    print("sitemap address "+str(sitemap))
    return 0

def sitemap_parse_XML(sitemap_content):
    #parse the xml
    
    print("sitemap XML ")
    return 0
    
#U NEED TO MAKE IT RECURSIVE
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
                #print(child.text)
            #print(child.tag," =-= ", child.attrib)
    return product_found