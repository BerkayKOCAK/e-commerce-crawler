
import os
import asyncio
from pathlib import Path
from src import scrape_elements
from bs4 import BeautifulSoup

def file_integrity():
    """
    Checks if assets, src and scraper folders are present.
    """
    absolutePath =  str(Path(__file__).parent.absolute())
    if os.path.exists(absolutePath+"\\assets\\"): pass
    else: os.mkdir(absolutePath+"\\assets\\")

    if os.path.exists(absolutePath+"\\scraper\\"): pass
    else: 
        print("Scraper folder not found!\nYou can not scrape the downloaded web pages without a scraper.\nPlease download it from = https://github.com/BerkayKOCAK/scraper-bot")
        return False
    return True

def create_vendor_folder(vendor):
    """
    vendor = Vendor name
    """
    vendorPath = str(Path(__file__).parent.absolute())+"\\assets\\"+str(vendor)
    if os.path.exists(vendorPath):
        pass
    else:
        os.mkdir(vendorPath)
        print("created vendor folder for : "+vendor+" as "+  vendorPath)



def create_product_folder(vendor,product):
    """
    product = Product name\n
    vendor  = Vendor name
    """
    productPath = str(Path(__file__).parent.absolute())+"\\assets\\"+str(vendor)+"\\"+str(product)
    if os.path.exists(productPath): pass
    else:
        print("created product folder for : "+product+" as "+  productPath)
        os.mkdir(productPath)
    return productPath



def html_writer(filePath,pageName,content):
    """
    Writes content of a html page with bytes.\n
    Removes some unwanted tags before writing the file\n
    filePath = Path to write\n
    pageName = Name of the file\n
    content = html dom content, byte format.
    """
    soup = BeautifulSoup(content, "html.parser")
    soup.find('script').decompose()
    soup.find('meta').decompose()
    soup.find('style').decompose()
    soup.find('noscript').decompose()
    soup.find('iframe').decompose()
    soup.find('footer').decompose()
    soup.find('header').decompose()
    with open(filePath+"\\"+pageName+".html", "wb") as f:
        f.write(content)


def url_name_strip(pageName):
    """
    Strips URL format string to a more humanly readable format.\n
    pageName = URL to strip down
    """
    index = 0
    start = pageName.rfind("/")+1
    end = pageName.rfind("?")
    occurences = 0 #pageName.count("-")
 
    for char in pageName:
        index += 1
        if (char == "-") and (index > start):
            occurences += 1
            if (occurences > 2):
                end = index
                break
         
    return pageName[start:end]
  
    
        
    