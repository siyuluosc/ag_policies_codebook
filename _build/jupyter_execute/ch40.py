#!/usr/bin/env python
# coding: utf-8

# # Ch 40 Oregon

#  [The Oregon State Legislature](https://www.oregonlegislature.gov/bills_laws/Pages/Oregon-Laws.aspx) stores all session laws of Oregon. On the website, there is a *Oregon Laws* section covering session laws from 1999 to 2023.
# 
# ![Oregon Legislature](pics/or_web.png)

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


# ## Get all session law url

# In[ ]:


sessionlist = driver.find_elements_by_css_selector('span.ms-commentexpand-iconouter')

for session in sessionlist:
    session.click()
    sleep(1)

chapters = driver.find_elements_by_css_selector('td.ms-cellstyle.ms-vb2 a')
for chapter in chapters:
    url = chapter.get_attribute('href')
    urls.append(url)

urlslist = list(set(urls))

urlslist.sort()


# ## PDF file download and Direct webscraping
# 
# In this section, we used the below code to extract all full texts from PDF files of session laws and extract all full texts, or webscrape all full texts of session laws directly.

# In[ ]:


for idx, url in enumerate(urlslist):
    driver.get(url)
    sleep(1)
    if '.pdf' in url:
        path = "/Users/long/OneDrive/Projects/AFRI/data/OR/"
        list_of_files = glob.glob(os.path.join(path, '*.pdf'))
        latest_file = max(list_of_files, key=os.path.getctime)
        print(latest_file)
        with open(os.path.join(os.getcwd(), latest_file), 'r') as f:  # open in readonly mode
            # creating a pdf File object of original pdf
            pdfFileObj = open(latest_file, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            pagenumber = pdfReader.numPages
            acttxt = []
            pgtxts = []
            for p in range(pagenumber):
                pageObj = pdfReader.getPage(p)
                pgtxt = pageObj.extractText()
                pgtxts.append(pgtxt)
                acttxt = '\n'.join(pgtxts)
    else:
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser")
        tag = soup.body
        acttxt = []
        for string in tag.strings:
            acttxt.append(string)
    acttxts.append(acttxt)


# ## Data saving

# In[ ]:


datasource = pd.DataFrame({
    'Session Laws': acttxts,
    'Link to full text': urls,
})

datasource.to_excel('OR_Leginfo.xlsx')
datasource.to_csv('OR_Leginfo.csv')
datasource.to_pickle('OR_Leginfo.pkl')
datasource.to_json('OR_Leginfo.json')

