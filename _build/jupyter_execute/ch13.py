#!/usr/bin/env python
# coding: utf-8

# # Ch 13 Georgia

# [Georgia General Assembly Website](https://www.legis.ga.gov/legislation/all) stores acts from 2001. The web address is https://www.legis.ga.gov/legislation/all. Georgia General Assembly Website provides Legislation Search shown as below. We can get all acts through File Transfer Protocol (FTP) and download all act PDF files into a local folder by hand.The main task is extract full act texts from all PDF files.
# ![Connecticut General Assembly](pics/ga_web.png)

# ## import libraries
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


driver_path = '/yourpath/driver'

# Change the working directory to your path on your computer
os.chdir('/yourpath/')

# Get the working directory
cwd = os.getcwd()
# Print the current working directory
print("Current working directory: {0}".format(cwd))

# Set up the driver
chromeOptions = webdriver.ChromeOptions()
dnldpath = {"download.default_directory": "/your_download_path"}
chromeOptions.add_experimental_option('prefs', {
    "download.default_directory": dnldpath,  #Change default directory for downloads
    "download.prompt_for_download": False,  #To auto download the file
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True,  #It will not show PDF directly in chrome
    "--enable-javascript": True
})
# Open the driver
driver = webdriver.Chrome(executable_path=driver_path, options=chromeOptions)


# ## PDF file download
# 
# ### Get all act urls first.

# In[ ]:


yrs = []
sts = []
seyrs = []
titles = []
bfsums = []
introdts = []
sigdts = []
effdts = []
epddtes = []
introducers = []
txtlks = []
acttxts = []
stas = []
hoscoms = []  # house committee
sponsors = []
sessions =[]
urls = []
billnums = []

WebDriverWait(driver, 300).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#session > option"))
)

# select all sessions except 2013-2024 session
all_sessions = driver.find_elements_by_css_selector('#session > option')
session_list = all_sessions[1:]

for index, i in enumerate(session_list):
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#session > option"))
    )
    all_sessions = driver.find_elements_by_css_selector('#session > option')
    session_list = all_sessions[1:]
    session_list[index].click()
    session = session_list[index].text
    print(session)

    search_btn = driver.find_element_by_css_selector('button.btn.btn-primary')
    search_btn.click()

    sleep(2)

    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.noResults'))
        )
        driver.find_element_by_css_selector('div.noResults')
        print("No results found")
    except:
        WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.resultCount b:nth-child(2)"))
        )
        total_bills = driver.find_element_by_css_selector('div.resultCount b:nth-child(2)').text

        if int(total_bills) % 20 == 0:
            total_pages = int(int(total_bills)/20)
        else:
            total_pages = int(int(total_bills)/20)+1
        print(total_pages)

        for page in range(total_pages):
            WebDriverWait(driver, 300).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".text-nowrap"))
            )
            bill_list = driver.find_elements_by_css_selector('.text-nowrap')
            for bill in bill_list:
                url = bill.get_attribute('href')
                urls.append(url)
                billnum = bill.text
                billnums.append(billnum)
                sessions.append(session)
            print("page",page+1)

            if total_pages > 0:
                WebDriverWait(driver, 300).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "ul > li:last-child > a > span"))
                )
                next_page = driver.find_element_by_css_selector('ul > li:last-child > a > span')
                try:
                    next_page.click()
                    sleep(1)
                except:
                    print("this session is done for urls")
            else:
                print("this session is done for urls")


# ### Downlowd all act PDF files

# In[ ]:


for idx,url in enumerate(urls):
    driver.get(url)
    sleep(1)

    version_btn =driver.find_elements_by_css_selector('li.list-inline-item')
    version_btn[0].click()

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.col-6.justify-content-end.text-right > button"))
    )
    dnldbtn = driver.find_element_by_class_name('btn.btn-outline-primary.btn-sm.mr-2.mb-1')
    dnldbtn.click()
print("Download finished")


# ## Text extraction and saving
# 
# In this section, we used the below code to extract all full texts from PDF files and save all act full texts into several format files including excel, csv, pickle and json.

# In[ ]:


path = "/Users/long/Library/CloudStorage/OneDrive-Personal/Projects/AFRI/data/GA"
files = glob.glob(os.path.join(path, '*.pdf'))

acttxts = []
pgtxts = []
badfiles = []
for file in files:
    try:
        doc = fitz.open(file)
        pgtxts = []
        for page in doc:
            pgtxt = page.get_text()
            pgtxts.append(pgtxt)
            acttxt = ' '.join(pgtxts)
        acttxts.append(acttxt)
        doc.close()
    except:
        print(file)
        badfiles.append(file)

datasource = pd.DataFrame({
    'Full text': acttxts
})

datasource.drop_duplicates(subset=['Full text'],
                           keep='first', inplace=True, ignore_index=True)

datasource.to_excel('GA_Leginfo.xlsx')
datasource.to_csv('GA_Leginfo.csv')
datasource.to_pickle('GA_Leginfo.pkl')
datasource.to_json('GA_Leginfo.json')

