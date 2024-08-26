#!/usr/bin/env python
# coding: utf-8

# # Ch 19 Kansas
# 
# The [Kansas Legislature Archival Website](https://www.kansas.gov/government/legislative/) stores the compilation of all Legislative bills enacted by a session of the Kansas Legislature, organized by chapter, from 1996 through 2010. The [Kansas Legislature](http://www.kslegislature.org/li_2022/historical/) stores all Legislative bills under *Bills and Sessions* since 2011.
# 
# ![Kansas Legislature Archival Website](pics/ks_ar.png)
# ![Kansas Legislature Archival Website](pics/ks_leg.png)
# 

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


# ## Direct webscraping and PDF file download

# In[ ]:


urls = []
acttxts = []

for year in range(1996, 2004):
    session_url = "https://www.kansas.gov/government/legislative/sessionlaws/" + str(year) + "/"
    driver.get(session_url)
    time.sleep(0.001)
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#agency-content > table > tbody"))
    )
    act_no = len(driver.find_elements_by_css_selector("#agency-content > table > tbody > tr > td:nth-child(1) > a"))
    for i in range(1, act_no + 1):
        print(i)
        url = "https://www.kansas.gov/government/legislative/sessionlaws/" + str(year) + "/chap" + str(i) + ".html"
        driver.get(url)
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
        )
        acttxt = driver.find_element_by_css_selector("body").text
        acttxts.append(acttxt)

for year in range(2004, 2011):
    url = "https://www.kansas.gov/government/legislative/sessionlaws/" + str(year) + "/"
    driver.get(url)
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#agency-content"))
    )
    acts = driver.find_elements_by_css_selector("#agency-content > table > tbody > tr > td:nth-child(1) > a")
    for act in acts:
        act.click()
        time.sleep(0.001)

bill_urls = []

for session_url in ["http://www.kslegislature.org/li_2022/b2021_22/measures/bills/",
                    "http://www.kslegislature.org/li_2021s/b2021s/measures/bills/",
                    "http://www.kslegislature.org/li_2016s/b2015_16/measures/bills/",
                    "http://www.kslegislature.org/li_2013s/b2013_14/measures/bills/",
                    "http://www.kslegislature.org/li_2020s/b2020s/measures/bills/",
                    "http://www.kslegislature.org/li_2020/b2019_20/measures/bills/",
                    "http://www.kslegislature.org/li_2018/b2017_18/measures/bills/",
                    "http://www.kslegislature.org/li_2016/b2015_16/measures/bills/",
                    "http://www.kslegislature.org/li_2014/b2013_14/measures/bills/",
                    "http://www.kslegislature.org/li_2012/b2011_12/measures/bills/"][:1]:
    print(session_url)
    driver.get(session_url)
    time.sleep(1)
    try:
        page_no = driver.find_element_by_css_selector("#tab-disp").text.split("of ")[1]
        for page in range(1, int(page_no) + 1):
            print(page)
            page_url = "http://www.kslegislature.org/li_2012/b2011_12/measures/bills/" + "#" + str(page)
            print(page_url)
            driver.get(page_url)
            time.sleep(0.01)
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#bill-tab-1"))
            )
            bills = driver.find_elements_by_css_selector("#bill-tab-1 > li a")
            for bill in bills:
                bill_url = bill.get_attribute("href")
                bill_urls.append(bill_url)
                print(bill_url)
    except:
        bills = driver.find_elements_by_css_selector("#bill-tab-1 > li a")
        for bill in bills:
            bill_url = bill.get_attribute("href")
            bill_urls.append(bill_url)
            print(bill_url)

for index, bill_url in enumerate(bill_urls):
    print(index)
    driver.get(bill_url)
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#version-tab-1 > tr"))
    )
    check = driver.find_element_by_css_selector("#version-tab-1 > tr").text
    if "Enrolled" in check:
        versions = driver.find_elements_by_css_selector("#version-tab-1 > tr")
        for version in versions:
            version_text = version.find_element_by_css_selector("td:nth-child(1)").text
            print(version_text)
            if "Enrolled" in version_text:
                pdf = driver.find_element_by_css_selector("#version-tab-1 > tr:nth-child(1) > td:nth-child(2) > a")
                pdf.click()
                time.sleep(0.01)


# ## Text extraction and saving
# 
# In this section, we used the below code to extract all full texts from PDF files and save all act full texts into several format files including excel, csv, pickle and json.

# In[ ]:


acttxts = []
path = "your_download_path"
files = glob.glob(os.path.join(path, '*.pdf'))
for file in files:
    doc = fitz.open(file)
    pgtxts = []
    for page in doc:
        pgtxt = page.get_text()
        pgtxts.append(pgtxt)
        acttxt = ' '.join(pgtxts)
    acttxts.append(acttxt)
    doc.close()

datasource = pd.DataFrame({
    'Full text': acttxts
})

datasource.drop_duplicates(subset=['Full text'],
                           keep='first', inplace=True, ignore_index=True)

# save all act info into files
datasource.to_excel('KS_Leginfo.xlsx')
datasource.to_csv('KS_Leginfo.csv')
datasource.to_pickle('KS_Leginfo.pkl')
datasource.to_json('KS_Leginfo.json')

