#!/usr/bin/env python
# coding: utf-8

# # Ch 43 South Carolina

#  [The South Carolina Legislature](https://www.scstatehouse.gov/aacts.php) stores all session laws of South Carolina. On the website, there is an *Acts Archives* section covering acts.
# 
# ![SC Legislature](pics/sc_web.png)
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
# All session laws on the website are stored as the html file. We can webscrape all session laws directly. Here we adopt a strategy to get all urls for all session laws, and then visit the url to extract the full text.

# In[ ]:


driver.get("https://www.scstatehouse.gov/aacts.php")
sessions = driver.find_elements_by_css_selector("div#contentsection a")

for idx, session in enumerate(sessions):
    sessionname = session.text
    if "Excel" in sessionname:
        print(sessionname)
    else:
        session_url = session.get_attribute('href')
        session_urls.append(session_url)
for idx, session_url in enumerate(session_urls):
    driver.get(session_url)
    sleep(1)
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "h2.barheader"))
    )
    yr = driver.find_element_by_css_selector("h2.barheader").text.rsplit("Acts")[1].rsplit("Session")[0].rsplit(" ")[0]
    if yr in specialyears:
        sessiongroup = driver.find_elements_by_css_selector("div#resultsbox dl dd a")
        for element in sessiongroup:
            sgurl = element.get_attribute('href')
            driver.get(sgurl)
            WebDriverWait(driver, 300).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div#contentsection"))
            )
            lawlist = driver.find_elements_by_css_selector("div#contentsection dl dt a")
            for element in lawlist:
                url = element.get_attribute('href')
                urls.append(url)
    else:
        WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div#resultsbox dl dd"))
        )
        lawlist = driver.find_elements_by_xpath('//*[@id="resultsbox"]/ dl / dt / a[1]')
        for element in lawlist:
            url = element.get_attribute('href')
            urls.append(url)

for idx, url in enumerate(urls):
    try:
        textloc = driver.find_element_by_css_selector("div.bill-list-item a.nodisplay")
        docurl = textloc.get_attribute('href')
        docurls.append(docurl)
        sleep(1)
        driver.get(docurl)
    except:
        docurls.append(url)
    body = driver.find_element_by_css_selector("body")
    acttxt = body.text
    acttxts.append(acttxt)


# ## Text saving
# 
# In this section, we used the below code to extract all full texts from PDF files and save all act full texts into several format files including excel, csv, pickle and json.

# In[ ]:


datasource = pd.DataFrame({
    'Full text': acttxts
})

datasource.drop_duplicates(subset = ['Full text'],
                     keep = 'first', inplace = True, ignore_index= True)

datasource.to_excel('NH_Leginfo.xlsx')
datasource.to_csv('NH_Leginfo.csv')
datasource.to_pickle('NH_Leginfo.pkl')
datasource.to_json('NH_Leginfo.json')

