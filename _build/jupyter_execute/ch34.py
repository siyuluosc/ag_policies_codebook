#!/usr/bin/env python
# coding: utf-8

# # Ch 34 New Mexico

# The New Mexico State Legislature store all acts passed in the State. The web address is https://www.nmlegis.gov/Legislation/Legislation_List. 

# There are three types of law sessions including regular session, special 1 session and special 2 session. All enrolled bills are named by "HB" and "SB" plus bill number. They are stored as pdf files on New Mexico Secretary of State website. 

# In[ ]:


#  import libraries
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
import time
import json
import re
import fitz
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession

s = HTMLSession()

driver_path = '/Users/siyu/Library/Mobile Documents/com~apple~CloudDocs/Projects/AFRI/chromedriver'
#driver = webdriver.Chrome(executable_path=DRIVER_PATH)

# Change the working directory
os.chdir('/Users/siyu/Library/Mobile Documents/com~apple~CloudDocs/Projects/AFRI')
# os.chdir('/Users/siyu/Desktop/AFRI web scraping')
# Get the current working directory
cwd = os.getcwd()
# Print the current working directory
print("Current working directory: {0}".format(cwd))

chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_experimental_option('prefs', {
"download.default_directory": '/Users/siyu/Library/Mobile Documents/com~apple~CloudDocs/Projects/AFRI', #Change default directory for downloads
"download.prompt_for_download": False, #To auto download the file
"download.directory_upgrade": True,
"plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
})

driver = webdriver.Chrome(executable_path=driver_path, options=chromeOptions)

#%%
# 2021 (check both .PDF and .pdf), then repeat for each year:
    # final versions (need to delete non-HB/SB):
(Reg) https://www.nmlegis.gov/Sessions/21%20Regular/final/
(Spe) https://www.nmlegis.gov/Sessions/21%20Special/final/
(Spe(2)) https://www.nmlegis.gov/Sessions/21%20Special2/final/
    # introduced (find 1.PDF & 2.PDF, svote/hvote/JUV/JUVV/CTV//COV/PAV/EDV/V.pdf, delete redundant files):
(Int(1)) https://www.nmlegis.gov/Sessions/21%20Regular/bills/house/
(Int(2)) https://www.nmlegis.gov/Sessions/21%20Regular/bills/senate/

    # add on (some years have these):
(Spe(3)) driver.get("https://www.nmlegis.gov/Sessions/17%20Special/bills/house/")
(Spe(4)) driver.get("https://www.nmlegis.gov/Sessions/17%20Special/bills/senate/")


act_urls = []
checklist = []
acts = []
acttxts = []

driver.get("https://www.nmlegis.gov/Sessions/12%20Regular/Final/")
driver.get("https://www.nmlegis.gov/Sessions/96%20Special/finalversions/")
driver.get("https://www.nmlegis.gov/Sessions/96%20Special2/final/")
driver.get("https://www.nmlegis.gov/Sessions/96%20Regular/bills/house/")
driver.get("https://www.nmlegis.gov/Sessions/96%20Regular/bills/senate/")

driver.get("https://www.nmlegis.gov/Sessions/96%20Special/bills/house/")
driver.get("https://www.nmlegis.gov/Sessions/96%20Special/bills/senate/")

#############################
# (Ext(1)(2)) for Extrodinary (eg. 2002):
driver.get("https://www.nmlegis.gov/Sessions/02%20Extraordinary/bills/house/")
driver.get("https://www.nmlegis.gov/Sessions/02%20Extraordinary/bills/senate/")


acts = driver.find_elements_by_partial_link_text(".PDF")
acts = driver.find_elements_by_partial_link_text(".pdf")


for act in acts:
    act.click()

#%%

badfiles = []
path = "/Users/siyu/Library/Mobile Documents/com~apple~CloudDocs/Projects/AFRI/midstop"
files = glob.glob(os.path.join(path,'*.pdf'))
for file in files:
    try:
        doc = fitz.open(file)
        pgtxts = []
        for page in doc:
            pgtxt = page.get_text()
            pgtxts.append(pgtxt)
            acttxts.append(acttxt)
            doc.close()
    except:
        print(file)
        badfiles.append(file)


# for 2022 sessions, all pdf downloaded
acttxts = []
path = "/Users/siyu/Library/Mobile Documents/com~apple~CloudDocs/Projects/AFRI/midstop"
files = glob.glob(os.path.join(path, '*.pdf'))
for file in files:
    doc = fitz.open(file)
    pgtxts = []
    for page in doc:
        pgtxt = page.get_text()
        pgtxts.append(pgtxt)
        acttxt = ' '.join(pgtxts)
    acttxts.append(acttxt)
    doc.close()
#%%

datasource = pd.DataFrame({
    'Full text': acttxts
})

# save bill info into files
datasource.to_excel('NM_Leginfo.xlsx')
datasource.to_csv('NM_Leginfo.csv')
datasource.to_pickle('NM_Leginfo.pkl')
datasource.to_json('NM_Leginfo.json')

