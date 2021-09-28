from selenium import webdriver
from helpers import html_parser, create_json


# Selenium Driver Configurations
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=r"chromedriver.exe", options=chrome_options)


product_page_url = 'https://www.1mg.com/otc/horlicks-women-s-plus-caramel-otc621844'


driver.get(product_page_url)
html_source = driver.page_source

soup = html_parser(html_source)
product_data = {
    "product_name": soup.select(".ProductTitle__product-title___3QMYH")[0].text,
    "product_manufacturer": soup.select(".ProductTitle__manufacturer___sTfon")[0].text,
    "product_rating": soup.select(".RatingDisplay__ratings-container___3oUuo")[0].text,
    "number_of_ratings": soup.select(".RatingDisplay__ratings-header___ZNj5b")[0].text,
    "product_imageURL": soup.select(".col-xs-10.ProductImage__preview-container___2oTeX")[0].select("img")[0]['src'],
}

print(product_data)