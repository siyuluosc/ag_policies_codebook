#!/usr/bin/env python
# coding: utf-8

# # Ch 4 Alaska

# The Alaska State Legislature store all acts passed in Alaska. The web address is https://www.akleg.gov/basis/Home/BillsandLaws. 
# 
# ![The Alaska State Legislature](pics/ak.png)

# The achieve sessions laws from 1981 to 2019 was found here: https://www.akleg.gov/basis/folioproxy.asp?url=http://wwwjnu03.akleg.org/cgi-bin/folioisa.dll/slpr/query=*/toc/{@21}?prev. 
# 
# 
# For 2021, the session laws were downloaded from https://www.akleg.gov/basis/Bill/Passed/32?sel=13. 

# In[ ]:


#  import libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from time import sleep
import pandas as pd
import datefinder
import calendar
import os
import unittest
from random import randint
import PyPDF2
import glob
import time
import pickle
import numpy as np
import fitz

driver_path = '/Users/siyu/Library/Mobile Documents/com~apple~CloudDocs/Projects/AFRI/chromedriver'
#driver = webdriver.Chrome(executable_path=DRIVER_PATH)

# Change the working directory
os.chdir('/Users/siyu/Library/Mobile Documents/com~apple~CloudDocs/Projects/AFRI/Alaska')
# os.chdir('/Users/siyu/Desktop/AFRI web scraping')
# Get the current working directory
cwd = os.getcwd()
# Print the current working directory
print("Current working directory: {0}".format(cwd))

chromeOptions = webdriver.ChromeOptions()
dnldpath = {"download.default_directory" : "/Users/siyu/Library/Mobile Documents/com~apple~CloudDocs/Projects/AFRI/Alaska"}
chromeOptions.add_experimental_option('prefs', {
"download.default_directory": dnldpath, #Change default directory for downloads
"download.prompt_for_download": False, #To auto download the file
"download.directory_upgrade": True,
"plugins.always_open_pdf_externally": True, #It will not show PDF directly in chrome
"--enable-javascript":True
})
driver = webdriver.Chrome(executable_path=driver_path, options=chromeOptions)

# use archive session laws from https://www.akleg.gov/basis/folioproxy.asp?url=http://wwwjnu03.akleg.org/cgi-bin/folioisa.dll/slpr/query=*/toc/{t1}?
    # contains 1981-2019

# this is the first page of 1981 chapters, the rest are written in an ordered urls
driver.get("https://www.akleg.gov/basis/folioproxy.asp?url=http://wwwjnu03.akleg.org/cgi-bin/folioisa.dll/slpr/query=*/doc/{@21}?prev")

act_urls = []
checklist = []
acts = []
urls = []

acttxts = []

# this is for general scraping not in url list
# 1981 1st page
# 2020
driver.switch_to.frame("docbody")
acttxt = driver.find_element_by_css_selector("body").text
print(driver.find_element_by_css_selector("body").text)
acttxts.append(acttxt)



# year 1981(start from the 2ed page)-2019
urlnumber = np.arange(1,4482,20)
print(urlnumber)

for i in urlnumber:
    url = "https://www.akleg.gov/basis/folioproxy.asp?url=http://wwwjnu03.akleg.org/cgi-bin/folioisa.dll/slpr/query=*/doc/{@" + str(i) + "}?next"
    print(url)
    urls.append(url)

for url in urls:
    driver.get(url)
    sleep(2)
    driver.switch_to.frame("docbody")
    acttxt = driver.find_element_by_css_selector("body").text
    print(driver.find_element_by_css_selector("body").text)
    acttxts.append(acttxt)


# for 2021, download pdf and scrape, https://www.akleg.gov/basis/Bill/Passed/32?sel=13
acts = ["SB0024Z", "HB0076Z", "HB0010Z", "HB0100Z", "HB0192Z", "HB0117Z", "HB0182Z", "HB0126Z", "SB0055Z", "HB0115Z", "SB0087Z", "SB0019Z", "SB0069Z",
        "SB0070Z", "HB0022Z", "HB0105Z", "HB0036Z", "SB0125Z", "SB0134Z", "HB0063Z", "HB0027Z", "HB0160Z", "HB0109Z", "SB0065Z", "SB0076Z", "SB0022Z",
        "SB0089Z", "SB0047Z", "SB0021Z", "HB0034Z", "SB0040Z", "SB0027Z", "SB0028Z", "SB0012Z", "HB0071Z", "HB0069Z", "HB3003Z"]

for act in acts:
    act_url = "https://www.akleg.gov/PDF/32/Bills/" + str(act) + ".PDF"
    print(act_url)
    act_urls.append(act_url)

for act_url in act_urls:
    driver.get(act_url)

path = "/Users/siyu/Library/Mobile Documents/com~apple~CloudDocs/Projects/AFRI/Alaska/2021pdfs"
files = glob.glob(os.path.join(path, '*.PDF'))
for file in files:
    doc = fitz.open(file)
    pgtxts = []
    for page in doc:
        pgtxt = page.get_text()
        pgtxts.append(pgtxt)
        acttxt = ' '.join(pgtxts)
    acttxts.append(acttxt)
    doc.close()

# parsing text of chapters into separate lines
bills = []
for acttxt in acttxts:
    t=acttxt.split("CHAPTER:")
    bills.extend(t)

# deleting lines with characters less than 20, only keeping the bill text
realbills = []
realbills = [item for item in bills if len(item) > 20]
print(realbills)


datasource = pd.DataFrame({
    'Full text': realbills
})

# save bill info into files
datasource.to_excel('AK_Leginfo.xlsx')
datasource.to_csv('AK_Leginfo.csv')
datasource.to_pickle('AK_Leginfo.pkl')
datasource.to_json('AK_Leginfo.json')

