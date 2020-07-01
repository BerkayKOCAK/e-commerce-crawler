"""
    Static Dictionary Variables
    #Websites has different kind of dom elements and management for each unique vendor.
    #Thus you need to add your elements to scrape like default ones. (hepsiburada,vatan,gittigidiyor...) 
    #Website names are case sensitive!
    #Non used items can be NULL.
    Includes:
        * websites
        * products
    Example to get vendor URL : scrape_elements.websites["hepsiburada"]["url"]
"""
default_page_query = "page"
websites = {
    "hepsiburada" : 
        {
            "name": "hepsiburada",
            'product-scope' : 
            
                {
                    'element': 'div',
                    'name': 'box product'
                },        
            'child-element' : 
            
                {
                    'title': 'h3',
                    'title_regex' : '.*title.*',
                    'price': 'span',
                    'price_regex' : '.*price.*',
                    'old_price': 'del'
                },
            'page-query' : "sayfa",
            'url' : "https://www.hepsiburada.com/",
            'sitemap' : "https://www.hepsiburada.com/sitemaps/sitemap.xml",
            'sitemap-category' : "https://www.hepsiburada.com/sitemaps/kategoriler/sitemap_1.xml",
            'non-xml-map' : False,
            'redirect-allowed': False #Some servers uses auto redirecting for query of non-existing pages, if thats the case make this False, else make it True
        },
    
    "gittigidiyor" : 
        {
            "name": "gittigidiyor",
            'product-scope' : 
            
                {
                    'element': 'li',
                    'name': '.*catalog-seem-cell.*'
                },        
            'child-element' : 
            # #TODO - has multiple ways to present price if you prune product search with more specific product names !!
                {
                    'title': 'h3',
                    'title_regex' : '.*title.*',
                    'price': 'p',
                    'price_regex' : '.*price.*',
                    'old_price': 'strike'
                },
            'page-query' : "sf",
            'url' : "https://www.gittigidiyor.com/",
            'sitemap' : "https://www.gittigidiyor.com/servisler/site-haritasi",
            'sitemap-category' : "",
            'non-xml-map' : True,
            'redirect-allowed': False
        },
    
    "n11" : 
        {
            "name": "n11",
            'product-scope' : 
            
                {
                    'element': 'li',
                    'name': 'column' #the fuck n11 ?
                },        
            'child-element' : 
            #TODO - "sepette ek indirim" price cannot be encapsulated with below specifications
                {
                    'title': 'h3',
                    'title_regex' : '.*productName.*',
                    'price': 'ins',
                    'price_regex' : None,
                    'old_price': 'del'
                },
            'page-query' : "pg",
            'url' : "https://www.n11.com/",
            'sitemap' : "https://www.n11.com/site-haritasi",
            'sitemap-category' : "",
            'non-xml-map' : True,
            'redirect-allowed': False
        },
    "teknosa" : 
        {
            "name": "teknosa",
            'product-scope' : 
            
                {
                    'element': 'div',
                    'name': 'product-item-inner'
                },        
            'child-element' : 
                {
                    'title': 'div',
                    'title_regex' : 'product-name',
                    'price': 'span',
                    'price_regex' : '.*price.*',
                    'old_price': '' #TODO - old and new price tags are same , 'span'. cant take old one !
                },
            'page-query' : default_page_query,
            'url' : "https://www.teknosa.com/",
            'sitemap' : "https://www.teknosa.com/siteharitasi.xml",
            'sitemap-category' : "https://www.teknosa.com/medias/sys_master/sitemaps/sitemaps/1752952165/Category-tr-TRY.xml",
            'non-xml-map' : False,
            'redirect-allowed': True
        },
    "media_markt" : 
        {
            "name": "media_markt",
            'product-scope' : 
            
                {
                    'element': 'div',
                    'name': 'product-wrapper'
                },        
            'child-element' : 
                {
                    'title': 'div',
                    'title_regex' : 'content', #TODO - takes also details ! try to prune more
                    'price': 'div',
                    'price_regex' : '.*price small length*.',
                    'old_price': '' 
                },
            'page-query' : default_page_query,
            'url' : "https://www.mediamarkt.com.tr/",
            'sitemap' : "https://www.mediamarkt.com.tr/sitemap/siteindex.xml",
            'sitemap-category' : "https://www.mediamarkt.com.tr/sitemap/sitemap-productlist.xml",
            'non-xml-map' : False,
            'redirect-allowed': True
        },
    "trendyol" : 
        {
            "name": "trendyol",
            'product-scope' : 
            
                {
                    'element': 'div',
                    'name': '.*p-card-wrppr.*'
                },        
            'child-element' : 
                {
                    'title': 'span',
                    'title_regex' : '.*prdct.*', 
                    'price': 'div',
                    'price_regex' : 'prc-box-sllng',
                    'old_price': '' 
                },
            'page-query' : "pi",
            'url' : "https://www.trendyol.com/",
            'sitemap' : "https://www.trendyol.com/sitemap",
            'sitemap-category' : "https://www.trendyol.com/sitemap_categories.xml",
            'non-xml-map' : False,
            'redirect-allowed': False
        },
    "amazon.tr" : 
        {
            "name": "amazon.tr",
            'product-scope' : 
            
                {
                    'element': 'div',
                    'name': 's-item-container'
                },        
            'child-element' : 
                {
                    'title': 'h2',
                    'title_regex' : '.*title.*', 
                    'price': 'span',
                    'price_regex' : '.*price*',
                    'old_price': '' 
                },
            #'page-query' : "......%XXX...default_page_query%%XXX.....",
            'url' : "https://www.amazon.com.tr/",
            'sitemap' : "https://www.amazon.com.tr/gp/site-directory/ref=topnav_sad",
            'sitemap-category' : "",
            'non-xml-map' : True,
            'redirect-allowed': True
        },
    "vatan" : 
        {
            "name": "vatan",
            'product-scope' : 
            
                {
                    'element': 'div',
                    'name': 'product-list product-list--list-page'
                },        
            'child-element' : 
            
                {
                    'title': 'div',
                    'title_regex' : '.*name.*',
                    'price': 'span',
                    'price_regex' : '.*price.*',
                    'old_price': ''
                },
            'page-query' : default_page_query,
            'url' : "https://www.vatanbilgisayar.com/",
            'sitemap' : "https://www.vatanbilgisayar.com/sitemap.aspx",
            'sitemap-category' : "",
            'non-xml-map' : True,
            'redirect-allowed': True
 
        }
}


#EXAMPLE USAGE
"""
FOR WEBSITES
    websites = [
        {
        "vendor_name" : 
            {
                "vendor_name_to_call": "examplesite",
                'product-scope' :
                        #This item is for locating listing element in dom content, give its tag and class name to locate.
                        #Example; if products are listed in <ul> tag u need to write its generic <li> element here
                    {
                        'element': 'div',
                        'name': 'box product'
                    },        
                'child-element' : 
                        #This item is for locating listed product element in dom content, give its tag and class name to locate.
                        #Class names are generic with regex to look for word price, title etc. 
                        #Regex is not a must if you are sure class names of the target elements wont change.

                    {
                        'title': 'h3',
                        'title_regex' : '.*title.*',
                        'price': 'span',
                        'price_regex' : '.*price.*',
                        'old_price': 'del'
                    }
            }
        }
    ]
////////////////////////////////////////////////////////////////////////
FOR PRODUCTS :
    products = {
        
        "Hepsiburada" : 
            {
                'products' : {}
                #key: product name, value: file path
            },
        "Vatan" : 
            {
                'products' : {}
                #key: product name, value: file path
            }
}
"""
products = {}

special_char_map = {ord('ä'):'a', ord('ü'):'u', ord('ö'):'o', ord('ş'):'s', ord('ç'):'c',ord('ğ'):'g',ord('ı'):'i',ord('İ'):'I'}


"""
examples:

print(str(products.get("Hepsiburada")))

products.get("Hepsiburada")['key2'] = 'for'

print(str(products.get("Hepsiburada")))

for target_list in products.keys():
   print(str(target_list))

"""

"""
    #This vendor's web site has faulty page search query
     "istanbulbilisim" : 
        {#this website has serious scripting issues, check when you are free !
            "name": "istanbulbilisim",
            'product-scope' : 
            
                {
                    'element': 'div',
                    'name': 'col-xs-6 col-sm-6 col-md-4'
                },        
            'child-element' : 
                {
                    'title': 'p',
                    'title_regex' : '.*title.*', 
                    'price': 'p',
                    'price_regex' : '.*price-act.*',
                    'old_price': 'p' 
                },
            'page-query' : "p",
            'url' : "https://www.istanbulbilisim.com/",
            'sitemap' : "https://www.istanbulbilisim.com/tum-kategoriler.html", #"https://www.istanbulbilisim.com/sitemap.xml",
            'sitemap-category' : "https://www.istanbulbilisim.com/tum-kategoriler.html",
            'non-xml-map' : True,
            'redirect-allowed': False
        },
"""