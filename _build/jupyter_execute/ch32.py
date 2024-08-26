#!/usr/bin/env python
# coding: utf-8

# # Ch 48 Vermont

#  [The General Court of New Hampshire](http://www.gencourt.state.nh.us/bill_status/legacy/bs2016/) stores all acts in New Hampshire. Through *Advanced Bill Status Search*, we can get all session laws including "signed by the governor" and "law without signature"
# 
# ![General Court of New Hampshire](pics/nh_web.png)
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

# In[ ]:


url = "http://www.gencourt.state.nh.us/bill_status/legacy/bs2016/"
driver.get(url)
driver.find_element_by_css_selector("#txtsessionyear").clear()

acturls = []
# signed by governor
for year in range(1989, 2023):
    url = "http://www.gencourt.state.nh.us/bill_status/legacy/bs2016/"
    driver.get(url)
    driver.find_element_by_css_selector("#txtsessionyear").clear()

    sessionyear = driver.find_element_by_css_selector("#txtsessionyear")
    sessionyear.send_keys(year)

    code = ["05"]
    status = driver.find_element_by_css_selector("#txtgstatus")
    status.send_keys(code)
    driver.find_element_by_css_selector("#cmdsubmit").click()
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Bill"))
    )
    sleep(10)
    acts = []
    acts.extend(driver.find_elements_by_link_text("Bill Text"))
    acts.extend(driver.find_elements_by_link_text("[HTML]"))
    sleep(1)
    for act in acts:
        url = act.get_attribute("href")
        print(url)
        acturls.append(url)
        time.sleep(0.001)

    # become law without siginature
    url = "http://www.gencourt.state.nh.us/bill_status/legacy/bs2016/"
    driver.get(url)
    driver.find_element_by_css_selector("#txtsessionyear").clear()
    code = ["06"]
    status = driver.find_element_by_css_selector("#txtgstatus")
    status.send_keys(code)
    driver.find_element_by_css_selector("#cmdsubmit").click()
    sleep(10)
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "head"))
    )
    acts = []
    acts.extend(driver.find_elements_by_link_text("Bill Text"))
    acts.extend(driver.find_elements_by_link_text("[HTML]"))
    sleep(1)
    for act in acts:
        url = act.get_attribute("href")
        print(url)
        acturls.append(url)
        time.sleep(0.001)

acttxts = []
badurls = []
for url in acturls:
    driver.get(url)
    t = randint(1, 10) * 0.001
    time.sleep(t)
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
    )
    try:
        acttxt = driver.find_element_by_css_selector("body").text
        acttxts.append(acttxt)
        t = randint(1, 10) * 0.001
        time.sleep(t)
        if "Server Error" in acttxt:
            badurls.append(url)
        else:
            print("good")
    except:
        print(url)
        badurls.append(url)


# ## Text saving
# 
# In this section, we used the below code to save all act full texts into several format files including excel, csv, pickle and json.

# In[ ]:


datasource = pd.DataFrame({
    'Full text': acttxts
})

datasource.drop_duplicates(subset = ['Full text'],
                     keep = 'first', inplace = True, ignore_index= True)

# save bill info into files
datasource.to_excel('VT_Leginfo.xlsx')
datasource.to_csv('VT_Leginfo.csv')
datasource.to_pickle('VT_Leginfo.pkl')
datasource.to_json('VT_Leginfo.json')

