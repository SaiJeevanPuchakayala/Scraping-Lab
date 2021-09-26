# `Objective:` 
# To Scrape Top trending products from `tata 1mg`.

# Importing Required Libraries
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import pandas as pd
import json

base_url = "https://www.1mg.com"
url_to_be_scraped = "https://www.1mg.com/categories/featured/trending-products-707"

# Getting the page source
def extract_source(url):
    print("Getting :",url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text,"lxml")
    return soup

# Scraping Products list from single page
def scrape_products_list(url):
    soup = extract_source(url)
    products_list_section = soup.select(".row.style__grid-container___1Xvb-")[0].select(".col-md-3.col-sm-4.col-xs-6.style__container___1TL2R ")
    single_page_products_data = []
    for product_section in products_list_section:
        
        # details that need to be scraped
        productName = "-"
        productUrl = "-"
        packSize = "-"
        productRating = "-"
        numberOfRating = "-"
        actualPrice = "-"
        discountPercent = "-"
        offerPrice = "-"
                
            
        # Execption handling for making the scraper go smooth even if few details are missing
        try:
            productName = product_section.select(".style__pro-title___2QwJy")[0].text
        except Exception:
            pass
                
        
        try:
            productUrl = base_url + product_section.select(".style__product-link___UB_67")[0]['href']
        except Exception:
            pass
        
        try:
            packSize = product_section.select(".style__pack-size___2JQG7")[0].text
        except Exception:
            pass
        
        try:
            productRating = product_section.select(".CardRatingDetail__weight-700___27w9q")[0].text
        except Exception:
            pass
        
        try:
            numberOfRating = product_section.select(".CardRatingDetail__ratings-header___2yyQW")[0].text
        except Exception:
            pass
        
        try:
            actualPrice = product_section.select(".style__discount-price___25Bya")[0].text
        except Exception:
            pass
        
        try:
            discountPercent = product_section.select(".style__off-badge___2JaF-")[0].text
        except Exception:
            pass
        
        try:
            offerPrice = product_section.select(".style__price-tag___cOxYc")[0].text
        except Exception:
            pass


        single_product_data = {
            "productName": productName,
            "productUrl": productUrl,
            "packSize": packSize,
            "productRating": productRating,
            "numberOfRating": numberOfRating,
            "actualPrice": actualPrice,
            "discountPercent": discountPercent,
            "offerPrice": offerPrice,
        }
        single_page_products_data.append(single_product_data)
    return single_page_products_data


# Scraping Products list from all the pages in the pagination.
def scrape_all_products(first_page_url):
    page_soup = extract_source(first_page_url)
    all_products_list = []
    max_pagination = page_soup.select(".col-xs-12.style__div-paginate___37OJx")[0].select("ul")[0].select("li")[-2].text
    for i in range(1,int(max_pagination)+1):
        page_url = f"https://www.1mg.com/categories/featured/trending-products-707?filter=true&pageNumber={i}"
        product_list = scrape_products_list(page_url)
        all_products_list.extend(product_list)
    return all_products_list

products_list = scrape_all_products(url_to_be_scraped)

# Code for creating CSV file.
df = pd.DataFrame(products_list)
df.to_csv("1mg_trending_products.csv", index=False)
print("\n CSV File Creation Successfull! #happingScraping")



# Code for creating JSON file.
# Serializing json
json_object = json.dumps(products_list, indent = 4)
  
# Writing to sample.json
with open("1mg_trending_products.json", "w") as outfile:
    outfile.write(json_object)
print("\n JSON File Creation Successfull! #happingScraping")