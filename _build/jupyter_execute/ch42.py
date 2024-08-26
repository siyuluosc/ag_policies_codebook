#!/usr/bin/env python
# coding: utf-8

# # Ch 42 Rhode Island

#  [The State of Rhode Island General Assembly](http://webserver.rilegislature.gov/search/search.asp?SearchWhere=/Billtext97/) stores all session laws of Rhode Island. On the website, there is a *Search The Rhode Island General Assembly Website* page. Through this page, we can search all session laws.
# 
# ![RI Legislature](pics/ri_act.png)
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


# ## Direct webscraping
# All session laws on the website are stored as the html files. We can webscrape them directly. With observation, there is an url pattern for the session laws: `"http://webserver.rilin.state.ri.us/PublicLaws/law" + *year* + "/law" + *year*  + *act number* + ".htm"`.
# ![RI Legislature](pics/ri_act.png)

# In[ ]:


act_urls = []
checklist = []
session_acts = []
acttxts = []

for year in range(1, 23):
    print(str(f"{year:02}"))
    session_url = "http://webserver.rilin.state.ri.us/Lawrevision/plshort/pl" + "20" + str(f"{year:02}") + "nu.htm"
    driver.get(session_url)
    no = len(driver.find_elements_by_css_selector("tbody tr"))
    for i in range(1, no+1):
        print(str(f"{i:03}"))
        url = "http://webserver.rilin.state.ri.us/PublicLaws/law" + str(f"{year:02}") + "/law" + str(f"{year:02}") + str(f"{i:03}") +".htm"
        try:
            driver.get(url)
            sleep(1)
            act_urls.append(url)
            acttxt = driver.find_element_by_css_selector("body").text
            acttxts.append(acttxt)
        except:
            checklist.append(url)

for url in act_urls:
    driver.get(url)
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
    )
    acttxt = driver.find_element_by_css_selector("body").text
    acttxts.append(acttxt)


# ## Text extraction and saving
# 
# In this section, we used the below code to extract all full texts from PDF files and save all act full texts into several format files including excel, csv, pickle and json.

# In[ ]:


datasource = pd.DataFrame({
    'Full text': acttxts
})

# save bill info into files
datasource.to_excel('RI_Leginfo.xlsx')
datasource.to_csv('RI_Leginfo.csv')
datasource.to_pickle('RI_Leginfo.pkl')
datasource.to_json('RI_Leginfo.json')

