
import os
import asyncio
from pathlib import Path
from src import scrape_elements
from bs4 import BeautifulSoup
from termcolor import colored


#############################################################################




#   MENU UTILS

#############################################################################

def file_integrity():
    """
    Checks if assets, src and scraper folders are present.
    """
    absolutePath =  str(Path(__file__).parent.absolute())
    if os.path.exists(absolutePath+"\\assets\\"): pass
    else: os.mkdir(absolutePath+"\\assets\\")

    if os.path.exists(absolutePath+"\\scraper.py") and os.path.exists(absolutePath+"\\csv_lib.py"): pass
    else: 
        print("Scraper folder not found!\ncsv_lib.py not found!\nYou can not scrape the downloaded web pages without a scraper.\nPlease download it from = https://github.com/BerkayKOCAK/scraper-bot")
        return False
    return True

async def timeout(time):
    """Simple timeout, takes time as seconds"""
    await asyncio.sleep(time)


def instructions():
    print(colored('Welcome To E-Commerce Crawler', 'green'), colored('\nInstructions : ', 'yellow'))
    print(colored('     * ', 'red'), colored('Crawler can operate with scraper, you need to add it to src/ folder as scraper.py', 'cyan'))
    print(colored('     * ', 'red'), colored('If you are using my scraper you also need to put csv_lib.py under src/', 'cyan'))
    print(colored('     * ', 'red'), colored('Operetable vendors are registered under src/scrape_elements.py, if you need to add new vendor just provide every object members like default vendors', 'cyan'))
    print(colored('This crawler is open source version of my commercial crawler, if you are interested in more professional crawler for e-commerce websites contact me : berkay.kocak@hotmail.com', 'cyan'))
    print(colored('If you have any issue or found a killer bug please open a github issue on the repository page.', 'cyan'))
    print(colored('-------------------------------------------------------------------------------------------------------------------------------', 'red'))

#############################################################################




#   SCRAPER-VENDOR UTILS

#############################################################################

def vendor_folder_mapping():
    """
    For scraper, checks every vendor's folder, then registers abendor as key and \"products\":{} object in the scarep_elements.pt file.\n
    In the end it will be mapped to the dictionary(map) as key( vendor ) : value( products:{ } )
    """
    folder_list = os.listdir(str(Path(__file__).parent.absolute())+"\\assets\\")
    if (len(folder_list) == 0):
        raise Exception(" - NO VENDOR FOUND - \nPlease read instructions again!")
    else:
        for folder in folder_list:
            scrape_elements.products[folder] = {"products":{}}



def menu_add_vendors(vendor_selection):
    """
    #Adds vendors to choices array at vendor_selection dict. as follows,
        'choices': [
                    Separator(' = Products = '),
                    {
                        'name': 'Hepsiburada',
                    },
                    {
                        'name': 'Vatan',
                        "disabled":"cause"
                        ...
                    },
                    ...
    """    
    new_vendor_selection = vendor_selection
    
    for vendor in scrape_elements.websites.keys():
        temp = {"name":vendor}#,"disabled":"cause"}
        new_vendor_selection[0]["choices"].append(temp)
    if("None" not in new_vendor_selection[0]["choices"]):
        new_vendor_selection[0]["choices"].append({"name":"None"})
    return new_vendor_selection

#############################################################################




#   SCRAPER-PRODUCT UTILS

#############################################################################

#TODO - Make page aligner folder based not some funky symbol -> "_"
def product_folder_mapping(vendors):
    """ 
    For scraper,
    Maps the files with respect to product names.\n
    Categorizes via vendor names.
    Then aligns sub-pages with product categories.
    """
    for vendor in vendors:
        vendor_path = str(Path(__file__).parent.absolute())+"\\assets\\"+str(vendor)
        if os.path.exists(vendor_path):

            productFolderList =  os.listdir(vendor_path)
            #category_list = product_subpage_aligner(productFolderList)

            for category in productFolderList:
                productFiles = os.listdir(str(vendor_path + "\\" + category))
                for file_holder in productFiles:
                    if (file_holder.find(".html") < 0):
                        print("file  "+file_holder+" cannot be scraped because it is not a html file !")
                    else:
                        #file_name = str(os.path.splitext(file_holder)[0])
                        file_path = str(vendor_path + "\\" + category +"\\" + str(Path(file_holder)))
                        try:
                            scrape_elements.products.get(vendor)['products'][category].append(file_path)
                        except KeyError:
                            scrape_elements.products.get(vendor)['products'][category] = [file_path]
        


def menu_add_products(product_selection):
    """
    Adds products to choices array at product_selection dict. as follows,
        'choices': [
                    Separator(' = Products = '),
                    {
                        'name': 'Vatan',
                        "disabled":"cause"
                        ...
                    },
                    ...
    """    
    new_product_selection = product_selection
    flag = 0
    for vendor in scrape_elements.products.keys():
        for product in scrape_elements.products.get(vendor)['products'].keys():
            flag = 0
            temp = {"name":product}#,"disabled":"cause"}
            #print("choices : "+str(new_product_selection[0].get("choices")))

            for index in new_product_selection[0].get("choices"):
              
                #print("index: "+str(index))
                if hasattr(index, 'get'):
                    if product == index.get("name"): 
                        flag = 1   
                        break
            if flag == 0:
                new_product_selection[0].get("choices").append(temp)
    if("None"not in new_product_selection[0]["choices"]):
        new_product_selection[0]["choices"].append({"name":"None"})

    return new_product_selection



#NO NEED!
def product_subpage_aligner(file_list):
    """
        Returns category names of the products, for example if there is bilgisayar.html,  bilgisayar_1.html, bilgisayar_2.html
        Takes bilgisayar.html as category and adds it to returned array as "bilgisayar". 
        *Thus category name must NOT include "_" symbol and
        *Sub pages which belongs to a category must include "_"
    """
    regex_array = []
    for file_holder in file_list:
        if (file_holder.find(".html") < 0):
                print("File "+file_holder+" cannot be added as product, it is not a html file !")
        else:
            file_name = str(os.path.splitext(file_holder)[0])
            if (file_name.find("_") < 0 ):
                regex_array.append(file_name)
            else:
                continue

    return regex_array

#############################################################################




#   CRAWLER UTILS

#############################################################################

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

    for script in soup.findAll(["script","meta","style","noscript","iframe","footer","header"]):
        script.decompose()
    
    with open(filePath+"\\"+pageName+".html", "wb") as f:
        f.write(soup.encode('utf-8'))



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
