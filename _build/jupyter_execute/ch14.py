#!/usr/bin/env python
# coding: utf-8

# # Ch 14 Hawaii

#  [Hawaii State Legislature](https://www.capitol.hawaii.gov/session/slh.aspx)  website stores all acts since 1959 in Hawaii. The web address is https://www.capitol.hawaii.gov/session/slh.aspx.
# 
# ![Hawaii State Legislature](pics/hi_web.png)
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


# ## PDF file download
# There is a section *SESSION LAWS OF HAWAII*. From this section, we can all session laws OF Hawaii. So, the main goal is to download all session law PDF files. ![HI Legislature](pics/hi_laws.png)

# In[ ]:


act_urls = []
checklist = []
session_acts = []
acttxts = []

driver.get("https://www.capitol.hawaii.gov/slh.aspx")

# for sessions (1975, 2018)
for year in range(1975, 2018):
    url = "https://www.capitol.hawaii.gov/slh/AllIndex/All_Acts_SLH" + str(year) + ".pdf"
    driver.get(url)
    time.sleep(1)

# for sessions (2018)
url = "https://www.capitol.hawaii.gov/slh/AllIndex/All_Acts_SLH2017SS-SLH2018.pdf"
driver.get(url)
time.sleep(1)

# for sessions (2019-2022)

for year in range(2019, 2023):
    url = "https://www.capitol.hawaii.gov/slh/AllIndex/SLH" + str(year) + "_Complete.pdf"
    driver.get(url)
    time.sleep(1)


# ## Text extraction and saving
# 
# In this section, we used the below code to extract all full texts from PDF files and save all act full texts into several format files including excel, csv, pickle and json.

# In[ ]:


acttxts = []
path = "/Users/long/Library/CloudStorage/OneDrive-Personal/Projects/AFRI/data/HI"
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
datasource.to_excel('HI_Leginfo.xlsx')
datasource.to_csv('HI_Leginfo.csv')
datasource.to_pickle('HI_Leginfo.pkl')
datasource.to_json('HI_Leginfo.json')

