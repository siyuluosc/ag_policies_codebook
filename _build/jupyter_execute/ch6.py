#!/usr/bin/env python
# coding: utf-8

# # Ch 6 Arkansas

# Arkansas State Legislature Website store all acts passed in Alabama. The web address is https://www.arkleg.state.ar.us/Acts/Search?ddBienniumSession=2021%2F2022F.
# 
# ![Arkansas State Legislature](pics/ar_web.png)

# We can search all acts on [Arkansas State Legislature](pics/ar_web.png). [This papg](https://www.arkleg.state.ar.us/Acts/Search?tbType=&ddBienniumSession=2021%2F2022F&bienniumAll=on&hdnSessions=on%2Cb2023%2Cz2023R%2Cb2021%2Cz2021R%2Cz2021S1%2Cz2021S2%2Cz2022F%2Cz2022S3%2Cb2019%2Cz2019R%2Cz2020F%2Cz2020S1%2Cb2017%2Cz2017R%2Cz2017S1%2Cz2018F%2Cz2018S2%2Cb2015%2Cz2015R%2Cz2015S1%2Cz2016F%2Cz2016S2%2Cz2016S3%2Cb2013%2Cz2013R%2Cz2013S1%2Cz2014F%2Cz2014S2%2Cb2011%2Cz2011R%2Cz2012F%2Cb2009%2Cz2009R%2Cz2010F%2Cb2007%2Cz2007R%2Cz2008S1%2Cb2005%2Cz2005R%2Cz2006S1%2Cb2003%2Cz2003R%2Cz2003S1%2Cz2003S2%2Cb2001%2Cz2001R%2Cz2002S1%2Cb1999%2Cz1999R%2Cz1999S1%2Cz2000S2%2Cb1997%2Cz1997R%2Cb1995%2Cz1995R%2Cz1995S1%2Cb1993%2Cz1993R%2Cz1993S1%2Cz1994S2%2Cb1991%2Cz1991R%2Cz1991S1%2Cz1991S2%2Cb1989%2Cz1989R%2Cz1989S1%2Cz1989S2%2Cz1989S3%2Cb1987%2Cz1987R%2Cz1987S1%2Cz1987S2%2Cz1987S3%2Cz1987S4%2C&ddChamber=A&tbActNumber=&tbBillNumber=&ddSponsor=&tbAllWords=&tbExactPhrase=&tbOneWord=&tbWithoutWords=&ddExclusivity=Only) shows all acts stored on Arkansas State Legislature Website. On the website, all acts are stored as PDF files. So, the goal is to download all act PDF files and extract full texts from PDF files.
# 

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
# 

# In[ ]:



driver.get(
    "https://www.arkleg.state.ar.us/Acts/Search?tbType=&ddBienniumSession=2021%2F2022F&bienniumAll=on&hdnSessions=on%2Cb2021%2Cz2021R%2Cz2021S1%2Cz2021S2%2Cz2022F%2Cb2019%2Cz2019R%2Cz2020F%2Cz2020S1%2Cb2017%2Cz2017R%2Cz2017S1%2Cz2018F%2Cz2018S2%2Cb2015%2Cz2015R%2Cz2015S1%2Cz2016F%2Cz2016S2%2Cz2016S3%2Cb2013%2Cz2013R%2Cz2013S1%2Cz2014F%2Cz2014S2%2Cb2011%2Cz2011R%2Cz2012F%2Cb2009%2Cz2009R%2Cz2010F%2Cb2007%2Cz2007R%2Cz2008S1%2Cb2005%2Cz2005R%2Cz2006S1%2Cb2003%2Cz2003R%2Cz2003S1%2Cz2003S2%2Cb2001%2Cz2001R%2Cz2002S1%2Cb1999%2Cz1999R%2Cz1999S1%2Cz2000S2%2Cb1997%2Cz1997R%2Cb1995%2Cz1995R%2Cz1995S1%2Cb1993%2Cz1993R%2Cz1993S1%2Cz1994S2%2Cb1991%2Cz1991R%2Cz1991S1%2Cz1991S2%2Cb1989%2Cz1989R%2Cz1989S1%2Cz1989S2%2Cz1989S3%2Cb1987%2Cz1987R%2Cz1987S1%2Cz1987S2%2Cz1987S3%2Cz1987S4%2C&ddChamber=A&tbActNumber=&tbBillNumber=&ddSponsor=&tbAllWords=&tbExactPhrase=&tbOneWord=&tbWithoutWords=&ddExclusivity=Only")

urls = []

acts = driver.find_elements(By.CSS_SELECTOR,
                            "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
for act in acts:
    url = act.get_attribute('href')
    urls.append(url)
driver.find_element(By.CSS_SELECTOR, '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(2)').click()
acts = driver.find_elements(By.CSS_SELECTOR,
                            "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
for act in acts:
    url = act.get_attribute('href')
    urls.append(url)
driver.find_element(By.CSS_SELECTOR, '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(3)').click()
acts = driver.find_elements(By.CSS_SELECTOR,
                            "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
for act in acts:
    url = act.get_attribute('href')
    urls.append(url)
driver.find_element(By.CSS_SELECTOR, '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(4)').click()
acts = driver.find_elements(By.CSS_SELECTOR,
                            "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
for act in acts:
    url = act.get_attribute('href')
    urls.append(url)
driver.find_element(By.CSS_SELECTOR, '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(5)').click()
acts = driver.find_elements(By.CSS_SELECTOR,
                            "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
for act in acts:
    url = act.get_attribute('href')
    urls.append(url)
driver.find_element(By.CSS_SELECTOR, '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(6)').click()
acts = driver.find_elements(By.CSS_SELECTOR,
                            "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
for act in acts:
    url = act.get_attribute('href')
    urls.append(url)
driver.find_element(By.CSS_SELECTOR, '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(7)').click()
acts = driver.find_elements(By.CSS_SELECTOR,
                            "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
for act in acts:
    url = act.get_attribute('href')
    urls.append(url)
driver.find_element(By.CSS_SELECTOR, '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(8)').click()
acts = driver.find_elements(By.CSS_SELECTOR,
                            "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
for act in acts:
    url = act.get_attribute('href')
    urls.append(url)
driver.find_element(By.CSS_SELECTOR, '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(9)').click()
acts = driver.find_elements(By.CSS_SELECTOR,
                            "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
for act in acts:
    url = act.get_attribute('href')
    urls.append(url)
driver.find_element(By.CSS_SELECTOR, '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(10)').click()
acts = driver.find_elements(By.CSS_SELECTOR,
                            "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
for act in acts:
    url = act.get_attribute('href')
    urls.append(url)
driver.find_element(By.CSS_SELECTOR, '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(11)').click()
acts = driver.find_elements(By.CSS_SELECTOR,
                            "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
for act in acts:
    url = act.get_attribute('href')
    urls.append(url)
driver.find_element(By.CSS_SELECTOR, '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(12)').click()
acts = driver.find_elements(By.CSS_SELECTOR,
                            "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
for act in acts:
    url = act.get_attribute('href')
    urls.append(url)
driver.find_element(By.CSS_SELECTOR, '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(13)').click()
acts = driver.find_elements(By.CSS_SELECTOR,
                            "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
for act in acts:
    url = act.get_attribute('href')
    urls.append(url)
driver.find_element(By.CSS_SELECTOR, '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(14)').click()
acts = driver.find_elements(By.CSS_SELECTOR,
                            "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
for act in acts:
    url = act.get_attribute('href')
    urls.append(url)
driver.find_element(By.CSS_SELECTOR, '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(15)').click()
acts = driver.find_elements(By.CSS_SELECTOR,
                            "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
for act in acts:
    url = act.get_attribute('href')
    urls.append(url)
driver.find_element(By.CSS_SELECTOR, '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(16)').click()
acts = driver.find_elements(By.CSS_SELECTOR,
                            "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
for act in acts:
    url = act.get_attribute('href')
    urls.append(url)
driver.find_element(By.CSS_SELECTOR, '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(17)').click()
acts = driver.find_elements(By.CSS_SELECTOR,
                            "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
for act in acts:
    url = act.get_attribute('href')
    urls.append(url)
driver.find_element(By.CSS_SELECTOR, '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(18)').click()
acts = driver.find_elements(By.CSS_SELECTOR,
                            "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
for act in acts:
    url = act.get_attribute('href')
    urls.append(url)
driver.find_element(By.CSS_SELECTOR, '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(19)').click()
acts = driver.find_elements(By.CSS_SELECTOR,
                            "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
for act in acts:
    url = act.get_attribute('href')
    urls.append(url)
driver.find_element(By.CSS_SELECTOR, '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(20)').click()
acts = driver.find_elements(By.CSS_SELECTOR,
                            "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
for act in acts:
    url = act.get_attribute('href')
    urls.append(url)
driver.find_element(By.CSS_SELECTOR, '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(21)').click()

for i in range(1, 71):
    print(i)
    acts = driver.find_elements(By.CSS_SELECTOR,
                                "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
    for act in acts:
        url = act.get_attribute('href')
        urls.append(url)
    driver.find_element(By.CSS_SELECTOR, '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(4)').click()
    time.sleep(1)
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#advancedResults"))
    )
    acts = driver.find_elements(By.CSS_SELECTOR,
                                "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
    for act in acts:
        url = act.get_attribute('href')
        urls.append(url)
    driver.find_element(By.CSS_SELECTOR, '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(5)').click()
    time.sleep(1)
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#advancedResults"))
    )
    acts = driver.find_elements(By.CSS_SELECTOR,
                                "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
    for act in acts:
        url = act.get_attribute('href')
        urls.append(url)
    driver.find_element(By.CSS_SELECTOR, '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(6)').click()
    time.sleep(1)
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#advancedResults"))
    )
    acts = driver.find_elements(By.CSS_SELECTOR,
                                "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
    for act in acts:
        url = act.get_attribute('href')
        urls.append(url)
    driver.find_element(By.CSS_SELECTOR, '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(7)').click()
    time.sleep(1)
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#advancedResults"))
    )
    acts = driver.find_elements(By.CSS_SELECTOR,
                                "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
    for act in acts:
        url = act.get_attribute('href')
        urls.append(url)
    driver.find_element(By.CSS_SELECTOR, '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(8)').click()
    time.sleep(1)
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#advancedResults"))
    )
    acts = driver.find_elements(By.CSS_SELECTOR,
                                "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
    for act in acts:
        url = act.get_attribute('href')
        urls.append(url)
    driver.find_element(By.CSS_SELECTOR, '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(9)').click()
    time.sleep(1)
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#advancedResults"))
    )
    acts = driver.find_elements(By.CSS_SELECTOR,
                                "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
    for act in acts:
        url = act.get_attribute('href')
        urls.append(url)
    driver.find_element(By.CSS_SELECTOR,
                        '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(10)').click()
    time.sleep(1)
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#advancedResults"))
    )
    acts = driver.find_elements(By.CSS_SELECTOR,
                                "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
    for act in acts:
        url = act.get_attribute('href')
        urls.append(url)
    driver.find_element(By.CSS_SELECTOR,
                        '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(11)').click()
    time.sleep(1)
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#advancedResults"))
    )
    acts = driver.find_elements(By.CSS_SELECTOR,
                                "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
    for act in acts:
        url = act.get_attribute('href')
        urls.append(url)
    driver.find_element(By.CSS_SELECTOR,
                        '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(12)').click()
    time.sleep(1)
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#advancedResults"))
    )
    acts = driver.find_elements(By.CSS_SELECTOR,
                                "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
    for act in acts:
        url = act.get_attribute('href')
        urls.append(url)
    driver.find_element(By.CSS_SELECTOR,
                        '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(13)').click()
    time.sleep(1)
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#advancedResults"))
    )
    acts = driver.find_elements(By.CSS_SELECTOR,
                                "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
    for act in acts:
        url = act.get_attribute('href')
        urls.append(url)
    driver.find_element(By.CSS_SELECTOR,
                        '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(14)').click()
    time.sleep(1)
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#advancedResults"))
    )
    acts = driver.find_elements(By.CSS_SELECTOR,
                                "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
    for act in acts:
        url = act.get_attribute('href')
        urls.append(url)
    driver.find_element(By.CSS_SELECTOR,
                        '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(15)').click()
    time.sleep(1)
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#advancedResults"))
    )
    acts = driver.find_elements(By.CSS_SELECTOR,
                                "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
    for act in acts:
        url = act.get_attribute('href')
        urls.append(url)
    driver.find_element(By.CSS_SELECTOR,
                        '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(16)').click()
    time.sleep(1)
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#advancedResults"))
    )
    acts = driver.find_elements(By.CSS_SELECTOR,
                                "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
    for act in acts:
        url = act.get_attribute('href')
        urls.append(url)
    driver.find_element(By.CSS_SELECTOR,
                        '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(17)').click()
    time.sleep(1)
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#advancedResults"))
    )
    acts = driver.find_elements(By.CSS_SELECTOR,
                                "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
    for act in acts:
        url = act.get_attribute('href')
        urls.append(url)
    driver.find_element(By.CSS_SELECTOR,
                        '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(18)').click()
    time.sleep(1)
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#advancedResults"))
    )
    acts = driver.find_elements(By.CSS_SELECTOR,
                                "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
    for act in acts:
        url = act.get_attribute('href')
        urls.append(url)
    driver.find_element(By.CSS_SELECTOR,
                        '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(19)').click()
    time.sleep(1)
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#advancedResults"))
    )
    acts = driver.find_elements(By.CSS_SELECTOR,
                                "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
    for act in acts:
        url = act.get_attribute('href')
        urls.append(url)
    driver.find_element(By.CSS_SELECTOR,
                        '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(20)').click()
    time.sleep(1)
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#advancedResults"))
    )
    acts = driver.find_elements(By.CSS_SELECTOR,
                                "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
    for act in acts:
        url = act.get_attribute('href')
        urls.append(url)
    driver.find_element(By.CSS_SELECTOR,
                        '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(21)').click()
    time.sleep(1)
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#advancedResults"))
    )
    acts = driver.find_elements(By.CSS_SELECTOR,
                                "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
    for act in acts:
        url = act.get_attribute('href')
        urls.append(url)
    driver.find_element(By.CSS_SELECTOR,
                        '#advancedResults > div.row.tableSectionFooter > div > a:nth-child(22)').click()
    time.sleep(1)
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#advancedResults"))
    )
    acts = driver.find_elements(By.CSS_SELECTOR,
                                "#advancedResults > div > div.col-md-1.meetingButtons.leftAlign.noPrint > a:nth-child(2)")
    for act in acts:
        url = act.get_attribute('href')
        urls.append(url)
    driver.find_element(By.PARTIAL_LINK_TEXT, "›").click()
    time.sleep(2)

urlsnew = list(dict.fromkeys(urls))
for i,url in enumerate(urlsnew):
    driver.get(url)
    time.sleep(0.1*randint(1, 2))


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

datasource.drop_duplicates(subset=['Full text'],
                           keep='first', inplace=True, ignore_index=True)

datasource.to_excel('AR_Leginfo.xlsx')
datasource.to_csv('AR_Leginfo.csv')
datasource.to_pickle('AR_Leginfo.pkl')
datasource.to_json('AR_Leginfo.json')

