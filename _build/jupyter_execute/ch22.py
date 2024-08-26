#!/usr/bin/env python
# coding: utf-8

# # Ch 21 Maine

#  [Maine State Legislature](https://legislature.maine.gov/ros/pdf-editions-of-published-session-laws-and-other-materials/12024) stores all acts passed in Maine. https://legislature.maine.gov/ros/pdf-editions-of-published-session-laws-and-other-materials/12024. As shown below, Maine State Legislature provides a web page with PDF Editions of Published Session Laws and Other Materials. So, the main task of webscraping is to download all PDF files with session laws.
# 
# ![Maine State Legislature](pics/me_web.png)

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


# ## PDF file download
# As shown on [Maine State Legislature](https://legislature.maine.gov/ros/pdf-editions-of-published-session-laws-and-other-materials/12024), all sessions are stored since 2009. We find elements with urls for all session law PDF files by using the syntax `find_elements_by_partial_link_text("Session")`. With the urls, we can download all session law PDF files.

# In[ ]:


driver.get('https://legislature.maine.gov/ros/LOM/LOMpdfDirectory.htm')
sessions = driver.find_elements_by_partial_link_text("Session")
session_urls = []

for session in sessions:
    session_url = session.get_attribute('href')
    session_urls.append(session_url)

for idx, url in enumerate(session_urls):
    driver.get(url)
    print(idx)
    sleep(60)


# ## Text extraction and saving
# 
# In this section, we used the below code to extract all full texts from PDF files and save all act full texts into several format files including excel, csv, pickle and json.

# In[ ]:


path = "your_download_path"
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

datasource.drop_duplicates(subset = ['Full text'],
                     keep = 'first', inplace = True, ignore_index= True)

datasource.to_excel('ME_Leginfo.xlsx')
datasource.to_csv('ME_Leginfo.csv')
datasource.to_pickle('ME_Leginfo.pkl')
datasource.to_json('ME_Leginfo.json')

