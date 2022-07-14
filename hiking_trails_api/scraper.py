import pandas as pd
import requests
from bs4 import BeautifulSoup


def scrape_trail_name(url_string):
    # url_string = "https://www.wta.org/go-hiking/hikes/talapus-and-olallie-lakes"
    response = requests.get(url_string)
    if response.status_code != 200:
        print("Error fetching page")
        exit()
    soup = BeautifulSoup(response.content, "html.parser")

    # Scrape Names
    found_text = soup.find(class_="documentFirstHeading").getText()

    return found_text


def scrape_lat_lon(url_string):
    # url_string = "https://www.wta.org/go-hiking/hikes/talapus-and-olallie-lakes"
    response = requests.get(url_string)
    if response.status_code != 200:
        print("Error fetching page")
        exit()
    soup = BeautifulSoup(response.content, "html.parser")

    # Scrape Names
    found_text = soup.find(class_="latlong")
    children = found_text.findChildren("span", recursive=False)

    text_list = []
    for i in children:
        text_list.append(i.text)

    return tuple(text_list)


def scrape_google_directions(url_string):
    # url_string = "https://www.wta.org/go-hiking/hikes/talapus-and-olallie-lakes"
    response = requests.get(url_string)
    if response.status_code != 200:
        print("Error fetching page")
        exit()
    soup = BeautifulSoup(response.content, "html.parser")

    # Scrape Names
    found_text = soup.find(class_="latlong")
    child = found_text.findChildren("a", recursive=False, href=True)[0]['href']
    child = child.strip('/')
    return child



