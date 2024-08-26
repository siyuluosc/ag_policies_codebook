#!/usr/bin/env python
# coding: utf-8

# # Ch 51 West Virginia

#  [West Virginia Legislature](https://www.wvlegislature.gov/index.cfm) stores all acts in West Virginia.
# 
# ![West Virginia Legislature](pics/wv_web.png)
# 
# On the website, there is a *Publications of the West Virginia Legislature* page. From this page, we can download all acts during 1975-2022.
# 
# ![West Virginia Legislature](pics/wv_acts.png)

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
# On *Publications of the West Virginia Legislature* page, there is a section *Acts of the Legislature of West Virginia*. From this section, we can see all volumes (PDF version) for West Virginia acts. So, the main goal is to download all volume PDF files. ![WV Legislature](pics/wv_acts.png)

# In[ ]:


act_urls = []
checklist = []
session_acts = []
acttxts = []

driver.get("https://www.wvlegislature.gov/Educational/publications.cfm#acts")

#most sessions except 2003
sessions = driver.find_elements_by_partial_link_text("Vol.")

for session in sessions:
    url = session.get_attribute("href")
    driver.get(url)
    time.sleep(1)

#2003 sessions
othersessions = ["https://www.wvlegislature.gov/legisdocs/publications/acts/Acts_2003_Vol_1.pdf","https://www.wvlegislature.gov/legisdocs/publications/acts/Acts_2003_Vol_2.pdf","https://www.wvlegislature.gov/legisdocs/publications/acts/Acts_2003_2ES.pdf"]
for url in othersessions:
    driver.get(url)
    time.sleep(1)


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
# save bill info into files
datasource.to_excel('WY_Leginfo.xlsx')
datasource.to_csv('WY_Leginfo.csv')
datasource.to_pickle('WY_Leginfo.pkl')
datasource.to_json('WY_Leginfo.json')

