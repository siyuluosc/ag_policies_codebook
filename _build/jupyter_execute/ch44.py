#!/usr/bin/env python
# coding: utf-8

# # Ch 44 South Dakota

#  [The South Dakota Legislature](https://sdlegislature.gov/Statutes/Archived) stores all session laws of South Dakota. On the website, there is a *Archived Sessions* section covering session laws.
# 
# ![SD Legislature](pics/sd_web.png)
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


# ## Direct webscraping
# All session laws on the website are stored as the html file. We can webscrape all session laws directly. Here we adopt a strategy to get all urls for all session laws, and then visit the url to extract the full text.
# 
# ![SD Legislature](pics/sd_web.png)

# In[ ]:


urls=[]
sessionurls = []
driver.get("https://www.sdlegislature.gov/Session/Archived")
#sessions = driver.find_elements_by_link_text("Session Laws")
sessions = driver.find_elements_by_css_selector('tbody tr td:nth-child(7) a')

for session in sessions:
    sessionurl = session.get_attribute('href')
    sessionurls.append(sessionurl)

for sessionurl in sessionurls:
    driver.get(sessionurl)
    try:
        list = driver.find_elements_by_css_selector("tbody tr td:nth-child(1) span a")
        for row in list:
            url = row.get_attribute('href')
            urls.append(url)
    except:
        print(sessionurl)
print("urls are done")

acttxts = []
for url in urls:
    driver.get(url)
    acttxt = driver.find_element_by_css_selector("body").text
    acttxts.append(acttxt)
    sleep(1)


# ## Text extraction and saving
# 
# In this section, we used the below code to extract all full texts from PDF files and save all act full texts into several format files including excel, csv, pickle and json.

# In[ ]:


datasource = pd.DataFrame({
    'Full text': acttxts
})

# save bill info into files
datasource.to_excel('SD_Leginfo.xlsx')
datasource.to_csv('SD_Leginfo.csv')
datasource.to_pickle('SD_Leginfo.pkl')
datasource.to_json('SD_Leginfo.json')

