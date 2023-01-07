from bs4 import BeautifulSoup
import cfscrape
from selenium import webdriver
import time
import os
from selenium.webdriver.support.ui import Select

AgriMarket_PriceURL = "https://agmarknet.gov.in/PriceTrends/SA_Pri_Month.aspx"

scraper = cfscrape.create_scraper()


def ScrapeCommodityPriceData(commodityName, yearData, monthData):
    # Selenium Driver Configurations
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(
        executable_path="chromedriver.exe",
        options=chrome_options,
    )
    # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # driver = webdriver.Chrome(
    #     executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options
    # )

    # Extracting HTML response
    driver.get(AgriMarket_PriceURL)

    commoditySelec_dropdown = driver.find_element("id", "cphBody_Commodity_list")
    commoditySelection = Select(commoditySelec_dropdown)
    commoditySelection.select_by_visible_text(commodityName)

    time.sleep(8)

    yearSelec_dropdown = driver.find_element("id", "cphBody_Year_list")
    yearSelection = Select(yearSelec_dropdown)
    yearSelection.select_by_visible_text(yearData)

    time.sleep(5)

    monthSelec_dropdown = driver.find_element("id", "cphBody_Month_list")
    monthSelection = Select(monthSelec_dropdown)
    monthSelection.select_by_visible_text(monthData)

    submitData = driver.find_element("id", "cphBody_But_Submit")
    submitData.click()

    time.sleep(5)

    html_pageSource = driver.page_source

    time.sleep(5)

    priceDataTable = []
    table_df_soup = BeautifulSoup(html_pageSource, "lxml")
    table_title = table_df_soup.select("#cphBody_Label3")[0].text.strip()
    table_rows = table_df_soup.select("#cphBody_DataGrid_PriMon")[0].select("tbody tr")
    for td in table_rows:
        State = td.select("td")[0].text.strip()
        currentMonthValue = td.select("td")[1].text.strip()
        previousMonthValue = td.select("td")[2].text.strip()
        currentMonthLastYearValue = td.select("td")[3].text.strip()
        changePercentMonth = td.select("td")[4].text.strip()
        changePercentYear = td.select("td")[5].text.strip()

        table_state_item = {
            "State": State,
            "currentMonthValue": currentMonthValue,
            "previousMonthValue": previousMonthValue,
            "currentMonthLastYearValue": currentMonthLastYearValue,
            "changePercentMonth": changePercentMonth,
            "changePercentYear": changePercentYear,
        }
        priceDataTable.append(table_state_item)

    driver.close()
    return priceDataTable, table_title


if __name__ == "__main__":
    commodityName = "Banana"
    yearData = "2022"
    monthData = "September"
    print(ScrapeCommodityPriceData(commodityName, yearData, monthData))
