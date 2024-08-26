#!/usr/bin/env python
# coding: utf-8

# # Ch 45 Tennessee

#  [The Tennessee General Assembly](https://www.capitol.tn.gov/legislation/archives.html) stores all session laws of Tennessee. On the website, there is a *Legislation Archives* section including Bills and Resolutions, Public Chapters, and Legislative Record. Here we focus on Public Chapters.
# 
# ![Tennessee General Assembly](pics/tn_web.png)
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
# 
# On [100th General Assembly Public Acts (1997-1998)](https://sharetngov.tnsosfiles.com/sos/acts/100/pub/pc1-100.htm) of the website, all public acts are stored as html files. We can webscrape all acts directly. For the left sessions available on the website, all acts are stored as PDF files. So, we can download all act PDF files.

# In[ ]:


acttxts = []

for i in range(0,1140):
    url = "https://sharetngov.tnsosfiles.com/sos/acts/100/pub/Pubc" + str(i).zfill(4) + ".HTM"
    driver.get(url)
    time.sleep(0.01)
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
    )
    acttxt = driver.find_element_by_css_selector("body").text
    acttxts.append(acttxt)

for year in range(101,105):
    print(year)
    for i in range(0,1500):
        url = "http://sharetngov.s3.amazonaws.com/sos/acts/" + str(year) + "/pub/pc" + str(i).zfill(4) + ".pdf"
        time.sleep(0.001)
        driver.get(url)

for year in range(105,113):
    print(year)
    for i in range(0,1500):
        url = "https://publications.tnsosfiles.com/acts/" + str(year) + "/pub/pc" + str(i).zfill(4) + ".pdf"
        time.sleep(0.001)
        driver.get(url)


# ## Text extraction and saving
# 
# In this section, we used the below code to extract all full texts from PDF files and save all act full texts into several format files including excel, csv, pickle and json.

# In[ ]:


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

# save bill info into files
datasource.to_excel('TX_Leginfo.xlsx')
datasource.to_csv('TX_Leginfo.csv')
datasource.to_pickle('TX_Leginfo.pkl')
datasource.to_json('TX_Leginfo.json')

