#!/usr/bin/env python
# coding: utf-8

# # Ch 28 Missouri

#  [The Missouri House of Representative website](https://docs.legis.wisconsin.gov/archive/law) stores all passed Senate and House bills in Missouri since 2000. In each session, there is a *Bills Truly Agreed and Finally Passed by Effective Date* section.
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
# On *Bills Truly Agreed and Finally Passed by Effective Date* section, there is an act list with the link to download the act PDF files. The urls for act PDf files are with the below pattern:"https://house.mo.gov/billtracking/bills" + session number + "hlrbillspdf/" + LR Number + ".pdf". We can find the LR number from the summary table saved by a csv file on the same page.
# So, we first download all summary tables, use LR number to make up the act urls and then download all PDF files.

# In[ ]:


path = "your_download_path for csv files"
csv_files = glob.glob(os.path.join(path, '*.csv'))

sumfile = pd.concat([pd.read_csv(f) for f in csv_files ], ignore_index=True)

sumfile.head()

df = sumfile

final = df[df[' Last Action'].str.contains("Vetoed") == False]

final.head()
checklist = []
for no in final['LR Number']:
    print(no)
    for i in range(111,224):
        try:
            act_url = "https://house.mo.gov/billtracking/bills" + str(i) + "/hlrbillspdf/" + no + ".pdf"
            driver.get(act_url)
        except:
            checklist.append(no)


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
datasource.to_excel('MO_Leginfo.xlsx')
datasource.to_csv('MO_Leginfo.csv')
datasource.to_pickle('MO_Leginfo.pkl')
datasource.to_json('MO_Leginfo.json')

