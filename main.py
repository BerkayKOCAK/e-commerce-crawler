
import asyncio
from src import crawler



def main():
    #check if assets folder available, else create
    #ask for product name (it can be multiple like xx,aa,bb,cc...)
    
    #check for scrape_elements.py file
    #show available vendors for crawling and scraping
    
    #with selected vendors, initialize crawling
    #crawler.url_GET_crawler("teknosa")
    asyncio.run(crawler.init_crawler(["bilgisayar","tablet"],["teknosa","vatan"]))
main()