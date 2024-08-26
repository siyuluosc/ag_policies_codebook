#!/usr/bin/env python
# coding: utf-8

# # Ch 10 Delaware

# The Delaware State Legislature store all acts passed in Delaware. The web address is https://legis.delaware.gov/SessionLaws. 

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

driver_path = '/Users/siyu/Library/Mobile Documents/com~apple~CloudDocs/Projects/AFRI/chromedriver'
#driver = webdriver.Chrome(executable_path=DRIVER_PATH)

# Change the working directory
os.chdir('/Users/siyu/Library/Mobile Documents/com~apple~CloudDocs/Projects/AFRI/Delaware')
# os.chdir('/Users/siyu/Desktop/AFRI web scraping')
# Get the current working directory
cwd = os.getcwd()
# Print the current working directory
print("Current working directory: {0}".format(cwd))

chromeOptions = webdriver.ChromeOptions()
dnldpath = {"download.default_directory" : "/Users/siyu/Library/Mobile Documents/com~apple~CloudDocs/Projects/AFRI/Delaware"}
chromeOptions.add_experimental_option('prefs', {
"download.default_directory": dnldpath, #Change default directory for downloads
"download.prompt_for_download": False, #To auto download the file
"download.directory_upgrade": True,
"plugins.always_open_pdf_externally": True, #It will not show PDF directly in chrome
"--enable-javascript":True
})
driver = webdriver.Chrome(executable_path=driver_path, options=chromeOptions)

# for all sessions:
####driver.get("https://legis.delaware.gov/SessionLaws/")

# test 2021-22
#driver.get("https://legis.delaware.gov/SessionLaws/Chapters?volume=48")

sessionurls = []
acts = []
urls = []

acttxts = []

# year 1975-2022 (128th-151st General Assembly), links end with 36-47, 1, 2, 5, 6, 8-10, 12-15, 48
for year in range (36,48): # change the years
    print(year)
    sessionurl = "https://legis.delaware.gov/SessionLaws/Chapters?volume=" + str(year)
    print(sessionurl)
    driver.get(sessionurl)
    acts = driver.find_elements_by_css_selector("#ContentPlaceholder_T3A13E1F0003_Col00 > div > div > ol > li > p:nth-child(1) > a")


    for act in acts:
        url = act.get_attribute("href")
        try:
            url = act.get_attribute("href")
            urls.append(url)
        # if not working, print the undone acts
        except:
            print(act)

for url in urls:
    driver.get(url)
    # mimic human working behavior to avoid crash
    t = randint(1,10)*0.001
    time.sleep(t)
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
    )
    acttxt = driver.find_element_by_css_selector('body').text
    print(driver.find_element_by_css_selector('body').text)
    acttxts.append(acttxt)


# for all session:
#sessionlist = driver.find_elements_by_css_selector('table.k-grid.k-widget.table a')
#for session in sessonlist:
#    session.click()
#    sleep(1)


datasource = pd.DataFrame({
    'Full text': acttxts
})

# save bill info into files
datasource.to_excel('DE_Leginfo.xlsx')
datasource.to_csv('DE_Leginfo.csv')
datasource.to_pickle('DE_Leginfo.pkl')
datasource.to_json('DE_Leginfo.json')

