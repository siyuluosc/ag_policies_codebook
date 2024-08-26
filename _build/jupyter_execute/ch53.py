#!/usr/bin/env python
# coding: utf-8

# # Ch 53 Wyoming

#  [Wyoming Legislature](https://www.wyoleg.gov/) stores all public acts in Wyoming since 2001. On the website, there is a Legislation Archives page.
# 
# ![Wyoming Legislature](pics/wy_archive.png)

# ## Import libraries
# As introduced in the chapter 1, we need to import some libraries as follows.

# In[ ]:


import time
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
import pickle
import numpy as np
import fitz


# ## Browser setup
# 
# Before scraping, we need to set up the browser. Here we use ChromeDriver for Google Chrome. You can download ChromeDriver from https://chromedriver.chromium.org/downloads following the version of Google Chrome you use on your laptop.

# In[ ]:


driver_path = 'yourpath/driver'

# Change the working directory to your path on your computer
os.chdir('yourpath')

# Get the working directory
cwd = os.getcwd()
# Print the current working directory
print("Current working directory: {0}".format(cwd))

# Set up the driver
chromeOptions = webdriver.ChromeOptions()
dnldpath = {"download.default_directory": "your_download_path"}
chromeOptions.add_experimental_option('prefs', {
    "download.default_directory": dnldpath,  #Change default directory for downloads
    "download.prompt_for_download": False,  #To auto download the file
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True,  #It will not show PDF directly in chrome
    "--enable-javascript": True
})
# Open the driver
driver = webdriver.Chrome(executable_path=driver_path, options=chromeOptions)


# ## Direct webscraping
# On Legislation Archives page, selecting a year and clicking *Enrolled Bills* button, we can see all enrolled bills. ![WY Legislature](pics/wy_enroll.png)

# After enrolled bills show up, clicking one, we can see the bill full text.
# 
# ![WY Legislature](pics/wy_text.png)
# 

# In[ ]:


act_urls = []

for year in range(2001, 2023):
    url = "https://www.wyoleg.gov/Legislation/" + str(year)
    driver.get(url)
    time.sleep(1)
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "body > div > div"))
    )
    time.sleep(2)
    driver.find_element_by_css_selector(
        "body > div > div > div:nth-child(3) > section > div > div:nth-child(4) > input:nth-child(3)").click()
    time.sleep(2)
    acts = driver.find_elements_by_css_selector(
        "body > div > div > div:nth-child(3) > section > div > div.table-responsive.ng-scope > table > tbody.ng-scope > tr > td:nth-child(1) > a")
    for act in acts:
        act_url = "https://www.wyoleg.gov/Legislation/" + str(year) + "/" + str(act.text)
        act_urls.append(act_url)

for year in range(2019, 2022):
    url = "https://www.wyoleg.gov/Legislation/" + str(year) + "?specialSessionValue=1"
    driver.get(url)
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "body > div > div"))
    )
    time.sleep(3)
    driver.find_element_by_css_selector(
        "body > div > div > div:nth-child(3) > section > div > div:nth-child(4) > input:nth-child(3)").click()
    time.sleep(3)
    acts = driver.find_elements_by_css_selector(
        "body > div > div > div:nth-child(3) > section > div > div.table-responsive.ng-scope > table > tbody.ng-scope > tr > td:nth-child(1) > a")
    for act in acts:
        act_url = "https://www.wyoleg.gov/Legislation/" + str(year) + "/" + str(act.text)
        act_urls.append(act_url)

act_urls = [*set(act_urls)]

acttxts = []
checklist = []

for i,url in enumerate(act_urls):
    print(i)
    driver.get(url)
    time.sleep(1)
    try:
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body > div > div > div:nth-child(3) > section > div > div.ng-scope > div > div > div.tab-pane.ng-scope.active > div.col-md-8.ng-scope"))
        )
        acttxt = driver.find_element_by_css_selector("body > div > div > div:nth-child(3) > section > div > div.ng-scope > div > div > div.tab-pane.ng-scope.active > div.col-md-8.ng-scope").text
        acttxts.append(acttxt)
        time.sleep(0.001)
    except:
        checklist.append(url)

for url in checklist:
    print(url)


# ## Text extraction and saving
# 
# In this section, we used the below code to extract all full texts from PDF files and save all act full texts into several format files including excel, csv, pickle and json.

# In[ ]:


datasource = pd.DataFrame({
    'Full text': acttxts
})

datasource.drop_duplicates(subset = ['Full text'],
                     keep = 'first', inplace = True, ignore_index= True)
# save bill info into files
datasource.to_excel('WY_Leginfo.xlsx')
datasource.to_csv('WY_Leginfo.csv')
datasource.to_pickle('WY_Leginfo.pkl')
datasource.to_json('WY_Leginfo.json')

