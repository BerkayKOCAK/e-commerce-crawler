
import os
import asyncio
from pathlib import Path
from src import scrape_elements



def create_vendor_folder(vendor):
    vendor_path = str(Path(__file__).parent.absolute())+"\\assets\\"+str(vendor)
    if os.path.exists(vendor_path):
        pass
    else:
        os.mkdir(vendor_path)
        print("created vendor folder for : "+vendor+" as "+  vendor_path)



def create_product_folder(vendor,product):
    product_path = str(Path(__file__).parent.absolute())+"\\assets\\"+str(vendor)+"\\"+str(product)
    if os.path.exists(product_path):
        pass
    else:
        print("created product folder for : "+product+" as "+  product_path)
        os.mkdir(product_path)
    return product_path



def html_writer(file_path,page_name,content):
    #print(content)
    with open(file_path+"\\"+page_name+".html", "wb") as f:
        f.write(content)



def url_name_strip(page_name):
    index = 0
    start = 0
    end = 0
    for char in page_name:
        #print(char)
        index = index + 1
        if (char == "/"):
            start = index

        if (char == "-"):
            end = index
            
    return page_name[start:end]
    
        
    