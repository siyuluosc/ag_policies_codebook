#!/usr/bin/env python
# coding: utf-8

# # Ch 39 Oklahoma

# [Oklahoma State Legislature](http://www.oklegislature.gov/TextOfMeasures.aspx) website stores all acts passed in Oklahoma. The web address is http://www.oklegislature.gov/TextOfMeasures.aspx.
# 
# ![Oklahoma Legislature website](pics/ok_web.png)

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
# As shown on the above screenshot of [Oklahoma State Legislature](http://www.oklegislature.gov/TextOfMeasures.aspx), users can select chamber, format, session and status. Here, we are to download all PDF files of acts by selecting *Adobe PDF* under **Select Format** and *Enrolled* under **Select Status**. For the both chambers, we have two pieces of code to get all act PDF file urls.

# ### Get all PDF files for both chambers

# In[ ]:


urls = []

driver.get('http://www.oklegislature.gov/TextOfMeasures.aspx')

sessions = ["2022 Regular Session", "2023 Regular Session", "2022 Third Special Session", "2022 Second Special Session",
            "2021 First Special Session", "2021 Regular Session - Web", "2020 Regular Session",
            "2020 First Special Session", "2019 Regular Session", "2018 Regular Session", "2017 Second Special Session",
            "2017 First Special Session", "2017 Regular Session", "2016 Regular Session", "2015 Regular Session",
            "2014 Regular Session", "2013 Special Session", "2013 Regular Session", "2012 Regular Session",
            "2011 Regular Session", "2010 Regular Session", "2009 Regular Session", "2008 Regular Session",
            "2007 Regular Session", "2006 Second Special Session", "2006 Regular Session", "2005 Special Session",
            "2005 Regular Session", "2004 Special Session", "2004 Regular Session", "2003 Regular Session",
            "2002 Regular Session", "2001 Special Session", "2001 Regular Session", "2012 Special Session",
            "2000 Regular Session", "1999 Special Session", "1999 Regular Session", "1998 Regular Session",
            "1997 Regular Session", "1996 Regular Session", "1995 Regular Session", "1994 Second Special Session",
            "1994 First Special Session", "1994 Regular Session", "1993 Regular Session"]

#for senate
for session in sessions:
    print(session)
    select_session = Select(driver.find_element_by_css_selector('#ctl00_ContentPlaceHolder1_cbxSessionId'))
    select_session.select_by_visible_text(session)
    sleep(1)
    select_status = Select(driver.find_element_by_css_selector('#ctl00_ContentPlaceHolder1_lbxMeasureStatus'))
    select_status.select_by_visible_text("Enrolled")
    driver.find_element_by_css_selector('#ctl00_ContentPlaceHolder1_Button1').click()
    sleep(1)
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_tblTomData"))
    )
    acts = driver.find_elements_by_css_selector('#ctl00_ContentPlaceHolder1_tblTomData > tbody > tr h2 b a')
    for act in acts:
        url = act.get_attribute("href")
        urls.append(url)

#for house
for session in sessions:
    print(session)
    driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_rbChamber_1").click()
    select_session = Select(driver.find_element_by_css_selector('#ctl00_ContentPlaceHolder1_cbxSessionId'))
    select_session.select_by_visible_text(session)
    sleep(1)
    select_status = Select(driver.find_element_by_css_selector('#ctl00_ContentPlaceHolder1_lbxMeasureStatus'))
    select_status.select_by_visible_text("Enrolled")
    driver.find_element_by_css_selector('#ctl00_ContentPlaceHolder1_Button1').click()
    sleep(1)
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_tblTomData"))
    )
    acts = driver.find_elements_by_css_selector('#ctl00_ContentPlaceHolder1_tblTomData > tbody > tr h2 b a')
    for act in acts:
        url = act.get_attribute("href")
        urls.append(url)


# ### Get all PDF files from above urls

# In[ ]:


for index,url in enumerate(urls):
    driver.get(url)
    print(index)


# ## Text extraction and saving
# 
# In this section, we used the below code to extract all full texts from PDF files and save all act full texts into several format files including excel, csv, pickle and json.

# In[ ]:


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

datasource.to_excel('OK_Leginfo.xlsx')
datasource.to_csv('OK_Leginfo.csv')
datasource.to_pickle('OK_Leginfo.pkl')
datasource.to_json('OK_Leginfo.json')


# There are three types of law sessions including regular session, special session and special organization session. All enrolled bills are named by "HB","SB","SR","HR","SJR", or "HJR" plus bill number and ended with "-enr". They are stored as pdf files on Alabama Secretary of State website. You can check the acts on [Alabama Legislature website](https://alison.legislature.state.al.us/acts).

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


# ## PDF file download
# As shown on [Alabama Legislature website](http://alisondb.legislature.state.al.us/Alison/SelectSession.aspx), all sessions are stored since 2000. We scraped all passed acts since 2000 within a loop using the code `for yr in range(2000, 2023)`. There are four types of sessions including regular session (RS), first special session (FS), second special session (SS), and organizational session (OS). For these session types, we had the loop `for st in ("RS","FS","SS","OS")`. For acts, there are also six types based on the act sponsor including "HB", "SB", "SR", "HR", "SJR", "HJR". All act PDF files, i.e., enrolled bills are files with the pattern: http://alisondb.legislature.state.al.us/ALISON/SearchableInstruments/ + year + session type + "/PrintFiles/" + act type + order number + "-enr.pdf". Using this pattern, we can download all act PDF files.

# In[ ]:


for yr in range(2000,2023):
    print(yr)
    for n in range(1,1000):
        for t in ("HB","SB","SR","HR","SJR","HJR"):
            for st in ("RS","FS","SS","OS"):
                url = "http://alisondb.legislature.state.al.us/ALISON/SearchableInstruments/" + str(yr) + st + "/PrintFiles/" + t + str(n) + "-enr.pdf"
                driver.get(url)
                time.sleep(0.001)


# ## Text extraction and saving
# 
# In this section, we used the below code to extract all full texts from PDF files and save all act full texts into several format files including excel, csv, pickle and json.

# In[ ]:


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

datasource.to_excel('AL_Leginfo.xlsx')
datasource.to_csv('AL_Leginfo.csv')
datasource.to_pickle('AL_Leginfo.pkl')
datasource.to_json('AL_Leginfo.json')

