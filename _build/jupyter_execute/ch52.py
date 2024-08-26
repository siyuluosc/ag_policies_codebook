#!/usr/bin/env python
# coding: utf-8

# # Ch 52 Wisconsin

#  [Wisconsin State Legislature](https://docs.legis.wisconsin.gov/archive/law) stores all public acts in Wyoming since 2001. On the website, there is a *Law Archive* page. From this page, we can download all acts during 1975-2022.
# 
# ![Wisconsin State Legislature](pics/wi_web.png)

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
# On *Law Archive*, clicking a year under the *Acts* column, Wisconsin Acts are stored as PDF files. Then the main task is to download all these PDF files. There is a storage url pattern for the PDF files. The url for a PDF file is "https://docs.legis.wisconsin.gov/" + *a session* + "/related/acts/" + *a number* + ".pdf". So, the strategy to download these PDF files is to visit a session, count how many acts in the session and use this to generate the url for a PDF file. The detail of code is shown as following. ![WI Legislature](pics/wi_acts.png)

# In[ ]:


sessions = ['1975','1977','1979','1981','1983','1985','1987','1989','1991','1993','1995','1997','1999','2001','2003','2005','2007','2009','2011','2013','2015','2017','2019','2021']
for session in sessions:
    session_url = "https://docs.legis.wisconsin.gov/" + str(session) + "/related/acts"
    print(session_url)
    driver.get(session_url)
    acts = driver.find_elements_by_partial_link_text("Wisconsin")
    for i in range(len(acts)):
        pdfurl = "https://docs.legis.wisconsin.gov/" + str(session) + "/related/acts/" + str(i+1) + ".pdf"
        driver.get(pdfurl)


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

