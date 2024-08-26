#!/usr/bin/env python
# coding: utf-8

# # Ch 46 Texas

#  [The Legislative Reference Library of Texas](https://lrl.texas.gov/legis/billsearch/searchchapter.cfm?legSession=87-0&chapter=&submitbutton=Search+by+chapter) stores all session laws of Texas.
# 
# ![Texas State Legislature](pics/tx_web.png)
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
# 
# First, we can visit each session on the website with the pattern: "https://lrl.texas.gov/legis/billsearch/searchchapter.cfm?legSession=" + *session number* +"-" + *subsession number* + "&chapter=&submitbutton=Search+by+chapter". Clicking the numbers under *Chapter* column,we can download the act PDF files.So, the main task is to get the urls for act PDF files, and click the urls to get all PDF files. ![Texas State Legislature](pics/tx_act.png)

# In[ ]:


#64-86th session 2021
urls = []

for session in range(64,87):
    for sub in range(0,4):
        url = "https://lrl.texas.gov/legis/billsearch/searchchapter.cfm?legSession=" + str(session) +"-" + str(sub) + "&chapter=&submitbutton=Search+by+chapter"
        driver.get(url)
        sleep(1)
        act_urls = driver.find_elements_by_css_selector('td.results a')
            for i in act_urls:
                act_url = i.get_attribute('href')
                if 'pdf' in act_url:
                    print(act_url)
                    urls.append(act_url)

for act in urls:
    driver.get(act)
    t = 0.1* randint(1, 9)
    time.sleep(t)


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
datasource.to_excel('TX_Leginfo.xlsx')
datasource.to_csv('TX_Leginfo.csv')
datasource.to_pickle('TX_Leginfo.pkl')
datasource.to_json('TX_Leginfo.json')

