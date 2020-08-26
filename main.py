#-*- coding: UTF-8 -*-

"""
        e-commerce-crawler CLI
        Berkay KOÇAK - 2020 June

        CLI Web page crawler with scraper for e-commerce vendors.

Written with Python 3.7.3
This version of crawler is to run on server as scheduled-script.

"""
import asyncio
import logging
from src import crawler, utils, scraper, mail_service
import subprocess


def main():
        
        utils.file_integrity()
        utils.archieveLog()

        sender = mail_service.Emailer()

        sendTo = 'berkay.kocak@hotmail.com'
        emailSubject = "Daily Crawler Report"

        logging.basicConfig(filename='loggings.log', 
        level=logging.INFO, 
        format='%(asctime)s | %(funcName)s | %(levelname)s | %(message)s',datefmt="%Y-%m-%d %H:%M:%S")

        vendors = utils.readFileToArray("vendors.txt")
        products = utils.readFileToArray("products.txt")
        
        logging.info("------------------------------------- INIT ------------------------------------------------------------")

        logging.info("CRAWLER STARTS")
        excludedWords = utils.readFileToArray("excludedWords.txt")
        asyncio.run(crawler.init_crawler(products,vendors,excludedWords))
        logging.info("CRAWLER ENDS")

        utils.vendor_folder_mapping()
        utils.product_folder_mapping(vendors)
        
        logging.info("SCRAPER STARTS")
        asyncio.run(scraper.scraper_init(vendors,products)) 
        logging.info("SCRAPER ENDS")
        utils.cleanUp(vendors)
       
        logging.info("------------------------------------- ENDING ------------------------------------------------------------")
       
        report = utils.logStatistics(vendors,products)
        asyncio.run(sender.sendmail(sendTo, emailSubject, report))
       
main()
exit(0)