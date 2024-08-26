#!/usr/bin/env python
# coding: utf-8

# # Ch 27 Mississippi

#  [Mississippi Legislature](http://www.legislature.ms.gov/) stores all public acts in Mississippi since 1997. As shown below, Mississippi Legislature has a Mississippi Legislative Bill Status System web page shown as below. We can extract all session law information through this web page.
# 
# ![Mississippi Legislature](pics/ms_web.png)

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


# ## Extracting Acts from Html and PDF files
# Through Mississippi Legislative Bill Status System web page shown above, choosing one legislative session, we can see the results within one session. There are two types of results. One type is only with a list of all measures in 1997 and 1998. For this type, we need to tell which act or measure here in Mississippi Legislature is approved. Clicking approved act, the full text is stored as a html file. We can extract full text![Mississippi Legislative Bill Status System](pics/ms_list.png)
# 
# Another type is with a list of all measures (not dead).All we need is under *All Measures (Not Dead)*. ![Mississippi Legislative Bill Status System](pics/ms_session.png) Clicking [*All Measures (Not Dead)](http://billstatus.ls.state.ms.us/2022/pdf/mainmenu.htm), the report of All Measures (Not Dead) are shown up. There are acts one by one which are stored as PDF files.

# In[ ]:


#Mississippi Legislature 1998 Regular Session

driver.get("http://billstatus.ls.state.ms.us/1998/all_measures/allmsrs.htm")

acts = driver.find_elements_by_partial_link_text("Approved")
for act in acts:
    url = act.get_attribute('href')
    urls.append(url)

#Mississippi Legislature 1999- Regular Session
for year in range(1999, 2008):
    session_url = "http://billstatus.ls.state.ms.us/" + str(year) + "/pdf/all_measures/notdead.htm"
    print(session_url)
    driver.get(session_url)
    acts = driver.find_elements_by_partial_link_text("Approved")
    for act in acts:
        url = act.get_attribute('href')
        urls.append(url)
    for e in ["1e", "2e", "3e", "4e"]:
        session_url = "http://billstatus.ls.state.ms.us/" + str(year) + e + "/pdf/all_measures/notdead.htm"
        print(session_url)
        driver.get(session_url)
        try:
            acts = driver.find_elements_by_partial_link_text("Approved")
            for act in acts:
                url = act.get_attribute('href')
                urls.append(url)
        except:
            print("No this session")
#Mississippi Legislature 1999- Regular Session

urls2 = []
for year in range(2009, 2023):
    session_url = "http://billstatus.ls.state.ms.us/" + str(year) + "/pdf/all_measures/notdead.xml"
    print(session_url)
    driver.get(session_url)
    acts = driver.find_elements_by_partial_link_text("Approved")
    for act in acts:
        url = act.get_attribute('href')
        urls2.append(url)
    for e in ["1e", "2e", "3e", "4e"]:
        session_url = "http://billstatus.ls.state.ms.us/" + str(year) + e + "/pdf/all_measures/notdead.xml"
        print(session_url)
        driver.get(session_url)
        try:
            acts = driver.find_elements_by_partial_link_text("Approved")
            for act in acts:
                url = act.get_attribute('href')
                urls2.append(url)
        except:
            print("No this session")

acttxts = []

for i, url in enumerate(urls):
    try:
        driver.get(url)
        print(i)
        WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
        )
        acturl = driver.find_element_by_partial_link_text("Sent to Governor").get_attribute('href')
        print(acturl)
        try:
            driver.get(acturl)
            if "pdf" in acturl:
                print("pdf")
            else:
                acttxt = driver.find_element_by_css_selector("html").text
                acttxts.append(acttxt)
        except:
            print("check")
    except:
        print("check")

for i, url in enumerate(urls2):
    try:
        driver.get(url)
        print(i)
        WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
        )
        acturl = driver.find_element_by_partial_link_text("Sent to Governor").get_attribute('href')
        print(acturl)
        try:
            driver.get(acturl)
            if "pdf" in acturl:
                print("pdf")
            else:
                acttxt = driver.find_element_by_css_selector("html").text
                acttxts.append(acttxt)
        except:
            print("check")
    except:
        print("check")


# ## Text extraction and output
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

datasource.to_excel('MS_Leginfo.xlsx')
datasource.to_csv('MS_Leginfo.csv')
datasource.to_pickle('MS_Leginfo.pkl')
datasource.to_json('MS_Leginfo.json')

