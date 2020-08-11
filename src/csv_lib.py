"""
    In here there are functions to manage and implement csv features
"""
import csv
import os
import logging



def write_csv(vendor,product,scrape_array):
    """ creates a output file like "vendor-product.csv" and then writes mapped items in scrape_array"""
    if not os.path.exists('output'):
        os.makedirs('output')
    if not os.path.exists('output/'+vendor):
        os.makedirs('output/'+vendor)
    if os.path.exists('output/'+vendor+'/'+vendor+'-'+product+'.csv'):
        write_mode = 'a'
    else:
        write_mode = 'w'
    f = open('output/'+vendor+'/'+vendor+'-'+product+'.csv', write_mode, newline='')
    
    try:
        with f:
            headers = ['productName', 'price(TL)',"old_price(TL)"]
            writer = csv.DictWriter(f, fieldnames=headers) 
            if write_mode == 'w':   
                writer.writeheader()
            for target_list in scrape_array:
                writer.writerow(target_list)
    except Exception as e:
        logging.critical(" HTML file WRITE error, meesage : "+ str(e))



def read_csv (vendor,product):
    """ Reades from ../output/'vendor'/'product-vendor.csv' """
    if not os.path.exists('output'):
        logging.info("Output Folder Not Found! Scrape something first !!")
        return
    if not os.path.exists('output/'+vendor):
        logging.info("Vendor Folder In Output Not Found! Scrape something first !!")
        return
    try:
        with open('../output/'+vendor+'/'+vendor+'-'+product+'.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    logging.info(f'Column names are: {", ".join(row)}')
                    line_count += 1
                else:
                    logging.info(f'\t{row} : ROW AS ARRAY\n')
                    line_count += 1
            logging.info(f'Processed {line_count} lines.')
    except Exception as e:
        logging.critical(" Vendor : "+vendor+" - Product : " +product +" --> HTML file READ error, message : "+ str(e))
