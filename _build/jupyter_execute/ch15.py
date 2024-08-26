#!/usr/bin/env python
# coding: utf-8

# # Ch 15 Idaho

# [The official website of the Idaho Legislature](https://legislature.idaho.gov/statutesrules/sessionlaws/) is an official website that stores all Idaho session laws. The web address is https://legislature.idaho.gov/statutesrules/sessionlaws/.
# 
# ![The official website of the Idaho Legislature](pics/id_web.png)

# On the website, all session laws are saved into one or two volumes as PDF files. The main task of webscraping is to download all PDF files with sessions laws since 195 and extract full texts from them.

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


# ## Downloading Session Law PDF files

# In[ ]:


driver.get('https://legislature.idaho.gov/statutesrules/sessionlaws/')

sessions = driver.find_elements_by_partial_link_text("Volume")

session_urls = []

for session in sessions:
    session_url = session.get_attribute('href')
    session_urls.append(session_url)

for idx, url in enumerate(session_urls):
    driver.get(url)
    print(idx)
    sleep(60)


# ### Extract full texts
# With the urls we scraped from last subsection, we click each url and extract the full bill text.

# In[ ]:


acttxts = []
pgtxts = []

path = "your_download_path"
files = glob.glob(os.path.join(path, '*.pdf'))

for file in files:
    with fitz.open(file) as doc:
        for page in doc:
            pgtxt = page.get_text()
            pgtxts.append(pgtxt)
            acttxt = '  '.join(pgtxts)
    acttxts.append(acttxt)


# ## Text saving and output
# 
# After extracting all full texts from PDF files, we saved them into different formats of files.

# In[ ]:


datasource = pd.DataFrame({
    #'Link to full text':session_urls,
    'Full text': acttxts
})

datasource.drop_duplicates(subset = ['Full text'],
                     keep = 'first', inplace = True, ignore_index= True)

datasource.to_excel('ID_Leginfo.xlsx')
datasource.to_csv('ID_Leginfo.csv')
datasource.to_pickle('ID_Leginfo.pkl')
datasource.to_json('ID_Leginfo.json')

