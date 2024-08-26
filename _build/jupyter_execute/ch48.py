#!/usr/bin/env python
# coding: utf-8

# # Ch 48 Vermont

#  [Vermont General Assembly](https://legislature.vermont.gov/bill/passed/2022#both-house-and-senate) stores all acts in Vermont.
# 
# ![Vermont General Assembly](pics/vt_web.png)
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


# ## Direct Webscraping
# 
# Clicking an act, there are several versions of full text. Our task is to webscrape the version of *Governor: Acts of Assembly Chapter text* and also download the PDF file.
# 

# In[ ]:


act_urls = []

for i in range(2010, 2024, 2):
    print(i)
    url1 = "https://legislature.vermont.gov/bill/passed/" + str(i) + "#house"
    driver.get(url1)
    sleep(1)
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#bills-passed-senate"))
    )
    driver.refresh()
    sleep(1)
    try:
        driver.find_element_by_css_selector("#bills-passed-house_length > label > select > option:nth-child(2)").click()
        sleep(2)
        acts = driver.find_elements_by_css_selector("#bills-passed-house > tbody > tr > td:nth-child(4) > a")
        for act in acts:
            act_url = act.get_attribute("href")
            act_urls.append(act_url)
    except:
        print(i)
        print(url1)

    url2 = "https://legislature.vermont.gov/bill/passed/" + str(i) + "?#senate"
    driver.get(url2)
    sleep(1)
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#bills-passed-senate"))
    )
    driver.refresh()
    sleep(1)
    try:
        driver.find_element_by_css_selector(
            "#bills-passed-senate_wrapper > div:nth-child(3) > div.dt-left > div > label > select > option:nth-child(2)").click()
        sleep(2)
        acts = driver.find_elements_by_css_selector("#bills-passed-house > tbody > tr > td:nth-child(4) > a")
        for act in acts:
            act_url = act.get_attribute("href")
            act_urls.append(act_url)
    except:
        print(i)
        print(url2)

    url3 = "https://legislature.vermont.gov/bill/passed/" + str(i) + "#both-house-and-senate"
    driver.get(url3)
    sleep(1)
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#bills-passed-senate"))
    )
    driver.refresh()
    sleep(1)
    try:
        driver.find_element_by_css_selector(
            "#bills-passed-both_wrapper > div:nth-child(3) > div.dt-left > div > label > select > option:nth-child(2)").click()
        sleep(2)
        acts = driver.find_elements_by_css_selector("#bills-passed-house > tbody > tr > td:nth-child(4) > a")
        for act in acts:
            act_url = act.get_attribute("href")
            act_urls.append(act_url)
    except:
        print(i)
        print(url3)

for i in ["2010.1", "2018.1", "2021.1"]:
    print(i)
    url1 = "https://legislature.vermont.gov/bill/passed/" + str(i) + "#house"
    driver.get(url1)
    sleep(1)
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#bills-passed-house"))
    )
    driver.refresh()
    sleep(1)
    try:
        driver.find_element_by_css_selector("#bills-passed-house_length > label > select > option:nth-child(2)").click()
        sleep(2)
        acts = driver.find_elements_by_css_selector("#bills-passed-house > tbody > tr > td:nth-child(4) > a")
        for act in acts:
            act_url = act.get_attribute("href")
            act_urls.append(act_url)
    except:
        print(i)
        print(url1)

    url2 = "https://legislature.vermont.gov/bill/passed/" + str(i) + "?#senate"
    driver.get(url2)
    sleep(1)
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#bills-passed-senate"))
    )
    driver.refresh()
    sleep(1)
    try:
        driver.find_element_by_css_selector(
            "#bills-passed-senate_wrapper > div:nth-child(3) > div.dt-left > div > label > select > option:nth-child(2)").click()
        sleep(2)
        acts = driver.find_elements_by_css_selector("#bills-passed-house > tbody > tr > td:nth-child(4) > a")
        for act in acts:
            act_url = act.get_attribute("href")
            act_urls.append(act_url)
    except:
        print(i)
        print(url2)

    url3 = "https://legislature.vermont.gov/bill/passed/" + str(i) + "#both-house-and-senate"
    driver.get(url3)
    sleep(1)
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#bills-passed-senate"))
    )
    driver.refresh()
    sleep(1)
    try:
        driver.find_element_by_css_selector(
            "#bills-passed-both_wrapper > div:nth-child(3) > div.dt-left > div > label > select > option:nth-child(2)").click()
        sleep(2)
        acts = driver.find_elements_by_css_selector("#bills-passed-house > tbody > tr > td:nth-child(4) > a")
        for act in acts:
            act_url = act.get_attribute("href")
            act_urls.append(act_url)
    except:
        print(i)
        print(url3)
act_urls = list(set(act_urls))

for url in act_urls:
    driver.get(url)


# ## Text extraction and saving
# 
# In this section, we used the below code to extract all full texts from PDF files and save all act full texts into several format files including excel, csv, pickle and json.

# In[ ]:


path = "your_download_path"
files = glob.glob(os.path.join(path, '*.pdf'))
acttxts = []
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

# save bill info into files
datasource.to_excel('VT_Leginfo.xlsx')
datasource.to_csv('VT_Leginfo.csv')
datasource.to_pickle('VT_Leginfo.pkl')
datasource.to_json('VT_Leginfo.json')

