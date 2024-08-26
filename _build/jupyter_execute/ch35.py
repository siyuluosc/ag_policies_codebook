#!/usr/bin/env python
# coding: utf-8

# # Ch 35 New York

#  [The New York State Assembly website](https://nyassembly.gov/leg/?sh=advanced) stores all acts in New York State.
# 
# ![New York State Assembly](pics/ny_web.png)
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

# In[ ]:


urls = []
driver.get("https://nyassembly.gov/leg/?sh=advanced")
sessions = ['2021-22','2019-20','2017-18','2015-16','2013-14','2011-12','2009-10','2007-08','2005-06','2003-04','2001-02','1999-00']
for session in sessions:
    driver.get("https://nyassembly.gov/leg/?sh=advanced")
    select_session = Select(driver.find_element_by_css_selector('select#term'))
    select_session.select_by_visible_text(session)
    select_type = Select(driver.find_element_by_css_selector('#leg_type'))
    select_type.select_by_visible_text('All Types')
    select_status = Select(driver.find_element_by_css_selector('#bill_status'))
    select_status.select_by_visible_text('Chaptered')
    driver.find_element_by_css_selector('#search_btn_div > input[type=button]:nth-child(1)').click()
    sleep(1)
    bills = driver.find_elements_by_css_selector('#vcontent_div > ul > li > a')
    for bill in bills:
        url = bill.get_attribute('href')
        urls.append(url)
        
acttxts = []
for url in urls:
    urlnew = str(url).replace("https://nyassembly.gov/leg/?", "https://nyassembly.gov/leg/?default_fld=&leg_video=&", 1) + "&Text=Y"
    driver.get(urlnew)
    time.sleep(0.1)
    WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#legcontent > pre")))
    act = driver.find_element_by_css_selector('#legcontent > pre').text
    actnew = re.sub("[\(\[].*?[\)\]]", "", act)
    acttxts.append(actnew)


# ## Text saving
# 
# In this section, we used the below code to extract all full texts from PDF files and save all act full texts into several format files including excel, csv, pickle and json.

# In[ ]:



datasource = pd.DataFrame({
    'Full text': acttxts,
})


# save bill info into files
datasource.to_excel('NY_Leginfo.xlsx')
datasource.to_csv('NY_Leginfo.csv')
datasource.to_pickle('NY_Leginfo.pkl')
datasource.to_json('NY_Leginfo.json')

