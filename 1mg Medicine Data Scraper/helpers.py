import requests
from bs4 import BeautifulSoup
import random
from pprint import pprint
import pandas as pd
import json
from user_agents_list import USER_AGENTS

# Getting the page source
def extract_source(url,headers= {}, params=[]):
    print("Getting: ", url)
    if "user-agent" not in headers:
        headers["user-agent"] = random.choice(USER_AGENTS)
    soup = BeautifulSoup(requests.get(
            url,
            headers=headers,
            params=params
        ).text,
        "lxml"
    )
    return soup


# Creates JSON file containing Scraped data.
def create_json(data,file_name):
    # Serializing json
    json_object = json.dumps(data, indent = 4)
    
    # Writing to sample.json
    with open(f"{file_name}.json", "w") as outfile:
        outfile.write(json_object)

    print("\n JSON File Creation Successfull! #happingScraping")
    return "Done"


# Creates CSV file containing Scraped data.
def create_csv(data,file_name):

    df = pd.DataFrame(data)
    df.to_csv(f"{file_name}.csv", index=False)

    print("\n CSV File Creation Successfull! #happingScraping")
    return "Done"


