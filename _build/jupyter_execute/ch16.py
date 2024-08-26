#!/usr/bin/env python
# coding: utf-8

# # Ch 16 Illinois

#  [Illinois Gneral Assembly](https://www.ilga.gov/)  website stores all acts since 1971 in Illinois. The web address is https://www.ilga.gov/.
# 
# ![Illinois Gneral Assembly](pics/il_web.png)
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

# In[ ]:


previous_sessions = ["79", "80", "81", "82", "83", "84", "85", "86", "87", "88", "89", "90", "91", "92", "93", "94",
                     "95", "96", "97", "98", "99", "100", "101", "102"]
for session in previous_sessions:
    for n in range(1, 2000):
        n = str(n)
        PDF_url = "https://www.ilga.gov/legislation/publicacts/" + session + "/PDF/" + session.zfill(3) + "-" + n.zfill(
            4) + ".pdf"
        print(PDF_url)
        try:
            driver.get(PDF_url)
            sleep(1)
        except:
            raise StopIteration

acttxts = []
pgtxts = []

path = "/Users/long/OneDrive/Projects/AFRI/data/IL/"
files = glob.glob(os.path.join(path, '*.pdf'))

for file in files:
    with fitz.open(file) as doc:
        for page in doc:
            pgtxt = page.get_text()
            pgtxts.append(pgtxt)
            acttxt = '  '.join(pgtxts)
    acttxts.append(acttxt)


# ## Text extraction and saving
# 
# In this section, we used the below code to extract all full texts from PDF files and save all act full texts into several format files including excel, csv, pickle and json.

# In[ ]:


path = "your_download_path"
acttxts = []
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
datasource.to_excel('IL_Leginfo.xlsx')
datasource.to_csv('IL_Leginfo.csv')
datasource.to_pickle('IL_Leginfo.pkl')
datasource.to_json('IL_Leginfo.json')

