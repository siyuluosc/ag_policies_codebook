#!/usr/bin/env python
# coding: utf-8

# # Ch 3 Alabama

# Alabama Legislature website stores all acts passed in Alabama. The web address is https://arc-sos.state.al.us/CGI/actyear.mbr/input.
# 
# ![Alabama Legislature website](pics/al.png)

# There are three types of law sessions including regular session, special session and special organization session. All enrolled bills are named by "HB","SB","SR","HR","SJR", or "HJR" plus bill number and ended with "-enr". They are stored as pdf files on Alabama Secretary of State website. You can check the acts on [Alabama Legislature website](https://alison.legislature.state.al.us/acts).

# ## import libraries
# As introduced in the chapter 1, we need to import some libraries as follows.

# In[10]:


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

# In[11]:


driver_path = '/yourpath/driver'

# Change the working directory to your path on your computer
os.chdir('/yourpath/')

# Get the working directory
cwd = os.getcwd()
# Print the current working directory
print("Current working directory: {0}".format(cwd))

# Set up the driver
chromeOptions = webdriver.ChromeOptions()
dnldpath = {"download.default_directory": "/your_download_path"}
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
# As shown on [Alabama Legislature website](http://alisondb.legislature.state.al.us/Alison/SelectSession.aspx), all sessions are stored since 2000. We scraped all passed acts since 2000 within a loop using the code `for yr in range(2000, 2023)`. There are four types of sessions including regular session (RS), first special session (FS), second special session (SS), and organizational session (OS). For these session types, we had the loop `for st in ("RS","FS","SS","OS")`. For acts, there are also six types based on the act sponsor including "HB", "SB", "SR", "HR", "SJR", "HJR". All act PDF files, i.e., enrolled bills are files with the pattern: http://alisondb.legislature.state.al.us/ALISON/SearchableInstruments/ + year + session type + "/PrintFiles/" + act type + order number + "-enr.pdf". Using this pattern, we can download all act PDF files.

# In[ ]:


for yr in range(2000,2023):
    print(yr)
    for n in range(1,1000):
        for t in ("HB","SB","SR","HR","SJR","HJR"):
            for st in ("RS","FS","SS","OS"):
                url = "http://alisondb.legislature.state.al.us/ALISON/SearchableInstruments/" + str(yr) + st + "/PrintFiles/" + t + str(n) + "-enr.pdf"
                driver.get(url)
                time.sleep(0.001)


# ## Text extraction and saving
# 
# In this section, we used the below code to extract all full texts from PDF files and save all act full texts into several format files including excel, csv, pickle and json.

# In[ ]:


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

datasource.drop_duplicates(subset=['Full text'],
                           keep='first', inplace=True, ignore_index=True)

datasource.to_excel('AL_Leginfo.xlsx')
datasource.to_csv('AL_Leginfo.csv')
datasource.to_pickle('AL_Leginfo.pkl')
datasource.to_json('AL_Leginfo.json')

