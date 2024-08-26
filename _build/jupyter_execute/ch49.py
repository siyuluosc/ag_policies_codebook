#!/usr/bin/env python
# coding: utf-8

# # Ch 49 Virginia

#  [Virginia's Legislative Information System](https://lis.virginia.gov/lis.htm) stores all acts of assembly chapters in Virginia.
# 
# ![Virginia Legislature](pics/va_web.png)
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
# Under a session, clicking an act, we can download the act full text as a PDF file.
# 
# ![Virginia Legislature](pics/va_acts.png)

# In[ ]:


driver.get("https://lis.virginia.gov/lis.htm")

select_sessionyear = Select(driver.find_element_by_css_selector("#sLink > form > select"))

sessions = driver.find_elements_by_css_selector("#sLink > form > select > option")

session_texts = []

for session in sessions:
    print(session.text)
    session_texts.append(session.text)

act_urls = []
for text in session_texts:
    driver.get("https://lis.virginia.gov/lis.htm")
    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#sLink > form > select"))
    )
    sleep(1)
    select_sessionyear = Select(driver.find_element_by_css_selector("#sLink > form > select"))
    select_sessionyear.select_by_visible_text(text)
    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#mainLink > li:nth-child(1) > a"))
    )
    driver.find_element_by_css_selector("#mainLink > li:nth-child(1) > a").click()
    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Acts of Assembly chapters"))
    )
    driver.find_element_by_link_text("Acts of Assembly chapters").click()
    sleep(1)
    acts = driver.find_elements_by_css_selector("#mainC > ul > li > a")
    for i in range(0, 20):
        acts = driver.find_elements_by_css_selector("#mainC > ul > li > a")
        for act in acts:
            url = act.get_attribute("href")
            act_urls.append(url)
        try:
            driver.find_element_by_link_text("More...").click()
            sleep(1)
        except:
            print("skip")

acttxts = []
checklist = []
pdf_urls = []
for url in act_urls:
    try:
        driver.get(url)
        WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "CHAP"))
        )
        t = randint(0, 9) * 0.01
        time.sleep(t)
        driver.refresh()
        driver.find_element_by_partial_link_text("CHAP").click()
        WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "body"))
        )
        driver.refresh()
        time.sleep(t)
        acttxt = driver.find_element_by_css_selector("#mainC").text
        acttxts.append(acttxt)
        pdf_url = driver.find_element_by_link_text("pdf").get_attribute("href")
        driver.get(pdf_url)
        pdf_urls.append(pdf_url)
    except:
        checklist.append(url)


# ## Text extraction and saving
# 
# In this section, we used the below code to extract all full texts from PDF files and save all act full texts into several format files including excel, csv, pickle and json.

# In[ ]:


datasource = pd.DataFrame({
    'Full text': acttxts
})

datasource.drop_duplicates(subset = ['Full text'],
                     keep = 'first', inplace = True, ignore_index= True)

# save acts info into files
datasource.to_excel('VA_Leginfo.xlsx')
datasource.to_csv('VA_Leginfo.csv')
datasource.to_pickle('VA_Leginfo.pkl')
datasource.to_json('VA_Leginfo.json')

