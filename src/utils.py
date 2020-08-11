
import os
import asyncio
import shutil
import logging
from datetime import datetime
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

    if os.path.exists(absolutePath+"\\assets\\"): pass
    else: os.mkdir(absolutePath+"\\assets\\")

    if os.path.exists("log_archive"): pass
    else: os.mkdir("log_archive")

    if os.path.exists(absolutePath+"\\scraper.py") and os.path.exists(absolutePath+"\\csv_lib.py"): pass
    else: 
        logging.info("Scraper folder not found!\ncsv_lib.py not found!\nYou can not scrape the downloaded web pages without a scraper.\nPlease download it from = https://github.com/BerkayKOCAK/scraper-bot")
        return False
    return True

def readFileToArray(fileName):
    arrayToReturn = []

    filePath = str(Path(__file__).parent.absolute())+"\\assets\\serverAssets\\"+fileName
    with open(filePath,encoding='utf-8') as fp: 
        lines = fp.readlines() 
        for line in lines: 
            if ((line != "") or (line != " ")  or (line != "\n")):
                arrayToReturn.append(line.strip())
    return arrayToReturn


     
def cleanUp(vendors):
    """Deletes vendor folders in /assets  """
    folderPath = str(Path(__file__).parent.absolute())+"\\assets\\"
    for vendor in vendors:
        if os.path.exists(folderPath+vendor):shutil.rmtree(folderPath+vendor,False)
        else:pass
       

#def raiseEx(): raise Exception("error in cleanUp !")



async def timeout(time):
    """Simple timeout, takes time as seconds"""
    await asyncio.sleep(time)



def archieveLog ():
    today = datetime.today()
    date = today.strftime("%Y-%m-%d")
    if os.path.exists("loggings.log"):
       shutil.move("loggings.log","log_archive/loggings-"+date+".log",)
    else:pass
        
   




def logStatistics (vendors,products):
    """ 
        Reads loggings.log file and then extracts a number of statistics for;
        *Time Spent
        *Number of Errors
        *Critical Errors
    
    """
    initialTime = ""
    endTime = ""
    crawlerInitialTime = ""
    crawlerEndTime = ""
    scraperInitialTime = ""
    scraperEndTime = ""

    delimittedLine = [] # [0] = time,  [1] = func,  [2] = level,  [3] = message
    errorCount = 0
    criticalErrors = []

    report = "Logger Report :"

    with open("loggings.log",encoding='utf-8',errors='ignore') as fp: 
        lines = fp.readlines() 
        
        for line in lines:
            delimittedLine = line.split("|")
            print(lines)
            if delimittedLine and ( 1 < len(delimittedLine) < 5):

                if (delimittedLine[3].find("INIT") > -1 ):              initialTime = delimittedLine[0].strip()
                elif (delimittedLine[3].find("ENDING") > -1 ):          endTime = delimittedLine[0].strip()

                elif (delimittedLine[3].find("CRAWLER STARTS") > -1 ):  crawlerInitialTime = delimittedLine[0].strip()
                elif (delimittedLine[3].find("CRAWLER ENDS") > -1 ):    crawlerEndTime = delimittedLine[0].strip()

                elif (delimittedLine[3].find("SCRAPER STARTS") > -1 ):  scraperInitialTime = delimittedLine[0].strip()
                elif (delimittedLine[3].find("SCRAPER ENDS") > -1 ):    scraperEndTime = delimittedLine[0].strip()

                elif(delimittedLine[2].strip() == "ERROR"):             errorCount += 1
                elif(delimittedLine[2].strip() == "CRITICAL"):          criticalErrors.append(line)


        initialTime_obj = datetime.strptime(initialTime, '%Y-%m-%d %H:%M:%S')
        endTime_obj = datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S')

        crawlerInitialTime_obj = datetime.strptime(crawlerInitialTime, '%Y-%m-%d %H:%M:%S')
        crawlerEndTime_obj = datetime.strptime(crawlerEndTime, '%Y-%m-%d %H:%M:%S')

        scraperInitialTime_obj = datetime.strptime(scraperInitialTime, '%Y-%m-%d %H:%M:%S')
        scraperEndTime_obj = datetime.strptime(scraperEndTime, '%Y-%m-%d %H:%M:%S')

        timeSpent = endTime_obj - initialTime_obj
        crawlerTimeSpent = crawlerEndTime_obj - crawlerInitialTime_obj
        scraperTimeSpent = scraperEndTime_obj - scraperInitialTime_obj

        report += ("\n| Start         = " + str(initialTime))
        report += ("\n| End           = "   + str(endTime))
        report += ("\n| Time Spent    = "    + str(timeSpent))
        report += ("\n| Error Count   = "   + str(errorCount))
        report += ("\n------------------------------------------")
        report += ("\n| Crawler Time Spent          = " + str(crawlerTimeSpent))
        report += ("\n| Scraper Time Spent          = " + str(scraperTimeSpent))


        report += ("\n\nCritical Errors:")
        if len(criticalErrors) == 0:
            report += (" NONE")
            report += ("\nStatus          = Succesfull")
        else: #if (output file size > 10Kb) :: partially succesfull
            for critic in criticalErrors:
                report += ("\n * "+critic)
            report += ("\nStatus          = Failure")
        report += ("\n\n------------------------------------------------------------------------------")
        report += ("\n\nVendors :")
        for vendor in vendors:
                report += ("\n - "+vendor)
        report += ("\nProducts :")
        for product in products:
                report += ("\n - "+product)

        report = report.translate(scrape_elements.special_char_map)   
    return report
    

#############################################################################




#   SCRAPER-VENDOR UTILS

#############################################################################

def vendor_folder_mapping():
    """
    For scraper, checks every vendor's folder, then registers a vendor as key and \"products\":{} object in the scarep_elements.pt file.\n
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
                        logging.info("File  "+file_holder+" cannot be scraped because it is not a html file !")
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
            #logging.info("choices : "+str(new_product_selection[0].get("choices")))

            for index in new_product_selection[0].get("choices"):
              
                #logging.info("index: "+str(index))
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
                logging.error("File "+file_holder+" cannot be added as product, it is not a html file !")
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
        logging.info("Created vendor folder for : "+vendor+" as "+  vendorPath)



def create_product_folder(vendor,product):
    """
    product = Product name\n
    vendor  = Vendor name
    """
    productPath = str(Path(__file__).parent.absolute())+"\\assets\\"+str(vendor)+"\\"+str(product)
    if os.path.exists(productPath): pass
    else:
        logging.info("Created product folder for : "+product+" as "+  productPath)
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

    try:
        for script in soup.findAll(["script","meta","style","noscript","iframe","footer","header"]):
            script.decompose()
        
        with open(filePath+"\\"+pageName+".html", "wb") as f:
            f.write(soup.encode('utf-8'))
    except Exception as e:
         logging.error(" url_name_strip error : "+ str(e))



def url_name_strip(pageName):
    """
    Strips URL format string to a more humanly readable format.\n
    pageName = URL to strip down
    """
    index = 0
    start = pageName.rfind("/")+1
    end = pageName.rfind("?")
    occurences = 0 #pageName.count("-")
 
    try:
        for char in pageName:
            index += 1
            if (char == "-") and (index > start):
                occurences += 1
                if (occurences > 2):
                    end = index
                    break
    except Exception as e:
         logging.critical(" url_name_strip error : "+ str(e))
         
    return pageName[start:end]
