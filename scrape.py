from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
from bs4 import BeautifulSoup
import csv

config = dotenv_values(".env")

user_name = config["USER"]
user_pass = config["PWD"]
url = "https://www.familysearch.org/ark:/61903/3:1:33S7-9BCJ-4TM?i=492&wc=MXMM-XP8%3A215131801&cc=1921755"

driver = webdriver.Chrome(ChromeDriverManager().install())


page_number_selector = "#openSDPagerInputContainer2 > input:nth-child(2)"

def login():
    driver.get(url)
    user_input_field = driver.find_element_by_css_selector("#userName")
    user_input_field.send_keys(user_name)

    password_input_field = driver.find_element_by_css_selector("#password")
    password_input_field.send_keys(user_pass)

    login_button = driver.find_element_by_css_selector("#login")
    login_button.click()

    #artifical wait if necessary 10 seconds
    driver.implicitly_wait(30)

    consent_button = driver.find_element_by_css_selector("#truste-consent-button")
    consent_button.click()

    driver.implicitly_wait(30)

def selectPage(page_number):
    page_input = driver.find_element_by_css_selector(page_number_selector)
    page_input.clear()
    page_input.send_keys(page_number)
    page_input.send_keys(Keys.ENTER)
    driver.implicitly_wait(30)

def scrapePage(page_number):
    data = []
    page = BeautifulSoup(driver.page_source, 'html.parser')
    tbl = page.find('table',{'class':'record-list-table'})
    rows = tbl.find_all('tr')
    for tr in rows:
        td = tr.find_all('td')
        row = [i.text.strip() for i in td]
        data.append(row)
    return data

def formatData(data, page_number):
    new_data = []
    for row in data:
        new_row = [str(page_number)]
        counter = 0
        for i in row:
            while counter in [3, 5, 6, 7, 8]:
                new_row.append("")
                counter += 1
            new_row.append(i)
            counter +=1
        #print(new_row)
        new_data.append(new_row)
    return new_data

def writeCSV(data, page_number):
    with open(f"output{page_number}.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, dialect='excel')
        for row in data:
            writer.writerow(row)
        

if __name__ == "__main__":
    login()
    input("press enter when loaded")
    #299 to 494 i think
    for pg in range(400, 494):
        selectPage(pg)
        input("press enter when loaded")
        data = scrapePage(pg)
        data = formatData(data, pg)
        writeCSV(data, pg)
