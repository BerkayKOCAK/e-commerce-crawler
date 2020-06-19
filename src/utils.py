
import os
import asyncio
from pathlib import Path
from src import scrape_elements



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
    if os.path.exists(productPath):
        pass
    else:
        print("created product folder for : "+product+" as "+  productPath)
        os.mkdir(productPath)
    return productPath



def html_writer(filePath,pageName,content):
    """
    Writes content of a html page with bytes

    filePath = Path to write

    pageName = Name of the file

    content = html dom content, byte format.
    """
    #TODO - 110 files takes nearly 58 Mb... do something about it!
    with open(filePath+"\\"+pageName+".html", "wb") as f:
        f.write(content)



def url_name_strip(pageName):
    """
    Strips URL format string to a more humanly readable format. 
    
    pageName = URL to strip down
    """
    index = 0
    start = 0
    end = 0
    for char in pageName:
        #print(char)
        index = index + 1
        if (char == "/"):
            start = index

        if (char == "-"):
            end = index
            
    return pageName[start:end]
    
        
    