from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import csv

URL = 'https://en.wikipedia.org/wiki/List_of_brown_dwarfs'
browser = webdriver.Chrome("chromedriver.exe")
browser.get(URL)
time.sleep(10)

headers = ['star_name', 'constellation', 'right_ascension', 'declination', 'apparent_magnitude', 'distance', 'spectral_type', 'brown_dwarf', 'mass', 'radius', 'orbital_period', 'semimajor_axis', 'eccentricity', 'discovery_year']
star_data = []
new_star_data = []
def scraper():
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    for th_tag in soup.find_all('th'):
        temp_list = []
        tr_tag = th_tag.find_all('tr')
        for tr_tag in tr_tag:
                    try:
                        temp_list.append(tr_tag.contents[0])
                    except:
                        temp_list.append('')

        star_data.append(temp_list)

def scrape_more_data(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content, "html.parser")
        temp_list = []
        for tr_tag in soup.find_all("tr", attrs={"class": "fact_row"}):
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div", attrs={"class": "value"})[0].contents[0])
                except:
                    temp_list.append("")
        new_star_data.append(temp_list)
    except:
        time.sleep(1)
        scrape_more_data(hyperlink)

scraper()
for index, data in enumerate(star_data):
    scrape_more_data(data[5])
    print(f"{index+1} page done 2")
final_star_data = []
for index, data in enumerate(star_data):
    new_star_data_element = new_star_data[index]
    new_star_data_element = [elem.replace("\n", "") for elem in new_star_data_element]
    new_star_data_element = new_star_data_element[:7]
    final_star_data.append(data + new_star_data_element)
with open("final.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(final_star_data)