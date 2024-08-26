#!/usr/bin/env python
# coding: utf-8

# # Ch 25 Michigan

#  [Michigan Legislature](https://www.legislature.mi.gov/) stores all public acts in Michigan since 1989. Its address is https://www.legislature.mi.gov/(S(0wetsrqlezkedtdyim2smihr).
# 
# ![Maine State Legislature](pics/mi_web.png)

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
# As shown below, choosing one legislative session, we can see the search results. ![Maine State Legislature](pics/mi_act.png)

# 
# On the search results web page, there are public acts shown up. Clicking one public act, two versions including html and PDF versions are available to be downloaded. We focus on using html versions.
# 
# ![Maine State Legislature](pics/mi_pdf.png)
# 
# Based on the structure, we first get all urls for PDF files and use them to extract full texts from act html versions.

# In[ ]:


# choose sessionyears
input_sessionyears = ['2021-2022', '2019-2020', '2017-2018', '2015-2016', '2013-2014', '2011-2012', '2009-2010',
                      '2007-2008', '2005-2006', '2003-2004', '2001-2002', '1999-2000', '1997-1998']

urls = []

for input_sessionyear in input_sessionyears:
    driver.get("https://www.legislature.mi.gov/(S(uycj0anii1cfudf2mj0uyllp))/mileg.aspx?page=LegAdvancedSearch")

    select_public = driver.find_element_by_css_selector('#frg_legadvancedsearch_PublicActs')
    select_public.click()

    # select session year
    select_sessionyear = Select(
        driver.find_element_by_css_selector('#frg_legadvancedsearch_LegislativeSession_LegislativeSession'))
    select_sessionyear.select_by_visible_text(input_sessionyear)

    # search by keywords
    #input_keywords = driver.find_element_by_css_selector('#frg_legadvancedsearch_LegFullText')
    #input_keywords.send_keys(keyword)

    # click search button
    search_button = driver.find_element_by_css_selector('#frg_legadvancedsearch_SearchButton')
    search_button.click()

    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#maincontent > table:nth-child(2) > tbody > tr:nth-child(1) > td > span"))
    )

    try:
        searchresult = driver.find_elements_by_css_selector(
            'table#frg_executesearch_SearchResults_Results  tbody  tr td a')
    except:
        continue
    sleep(3)

    for i in range(len(searchresult)):
        url = searchresult[i].get_attribute('href')
        urls.append(url)

print("done with urls")

acttxts = []

for url in urls:
    driver.get(url)
    acttxt = driver.find_element_by_css_selector("body").text
    acttxts.append(acttxt)
    sleep(randint(1,2))


# ## Text extraction and saving
# 
# In this section, we used the below code to extract all full texts from PDF files and save all act full texts into several format files including excel, csv, pickle and json.

# In[ ]:


datasource = pd.DataFrame({
    'Full text': acttxts
})

datasource.drop_duplicates(subset = ['Full text'],
                     keep = 'first', inplace = True, ignore_index= True)

datasource.to_excel('ME_Leginfo.xlsx')
datasource.to_csv('ME_Leginfo.csv')
datasource.to_pickle('ME_Leginfo.pkl')
datasource.to_json('ME_Leginfo.json')

