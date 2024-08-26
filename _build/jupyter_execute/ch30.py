#!/usr/bin/env python
# coding: utf-8

# # Ch 30 Nebraska

# [The Nebraska Legislature](https://nebraskalegislature.gov/laws/browse-statutes.php) is the official site of the Nebraska Unicameral Legislature. The web address is https://nebraskalegislature.gov/laws/browse-statutes.php.
# 
# ![Nebraska Legislature](pics/ne_web.png)

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


urls = []
sessionurls = []
section_urls = []
chs = list(range(1, 91))
for ch in chs:
    ch = str(ch)
    ch_url = "https://nebraskalegislature.gov/laws/browse-chapters.php?chapter=" + ch
    driver.get(ch_url)
    sections = driver.find_elements_by_css_selector("span.col-md-2.col-sm-3.my-auto:nth-child(1) a")
    for section in sections:
        section_url = section.get_attribute('href')
        section_urls.append(section_url)

sections = []
bill_urls = []
for section_url in section_urls:
    driver.get(section_url)
    section_text = driver.find_element_by_css_selector("div.card-body").text
    sections.append(section_text)
    try:
        bills = driver.find_elements_by_partial_link_text("Laws ")
        for bill in bills:
            bill_url = bill.get_attribute('href')
            bill_urls.append(bill_url)
    except:
        print("no source")
print("done with bill urls")

billurls = list(set(bill_urls))
for idx, url in enumerate(billurls):
    driver.get(url)


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

datasource.to_excel('NE_Leginfo.xlsx')
datasource.to_csv('NE_Leginfo.csv')
datasource.to_pickle('NE_Leginfo.pkl')
datasource.to_json('NE_Leginfo.json')

