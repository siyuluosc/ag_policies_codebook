#!/usr/bin/env python
# coding: utf-8

# # Ch 21 Louisiana

#  [Louisiana State Legislature](https://www.legis.la.gov/Legis/Home.aspx) stores all acts passed in Louisiana. The web address is https://www.legis.la.gov/Legis/Home.aspx.
# 
# ![Louisiana State Legislature](pics/la_web.png)

# There are three types of law sessions including regular session, special session and special organization session. All enrolled bills are named by "HB","SB","SR","HR","SJR", or "HJR" plus bill number and ended with "-enr". They are stored as pdf files on Alabama Secretary of State website. You can check the acts on [Alabama Legislature website](https://alison.legislature.state.al.us/acts).

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
# As shown on [Louisiana State Legislature](https://www.legis.la.gov/Legis/Home.aspx), all sessions are stored since 1997. First, we go to each session available. Then, we click each act within the session. Clicking the Text button, there are several versions of bills and we only download the act PDF file. All the process can be implemented by the blow code.

# In[ ]:


driver.get('https://www.legis.la.gov/Legis/SessionInfo/SessionInfo.aspx')

session_links = driver.find_elements_by_partial_link_text("Session")
acts = []
years = ['97RS','971ES','972ES','973ES','98RS','981ES','982ES','983ES','99RS','991ES','992ES','993ES','00RS','001ES','002ES','003ES','01RS','011ES','012ES','013ES','02RS','021ES','022ES','023ES','03RS','031ES','032ES','033ES','04RS','041ES','042ES','043ES','05RS','051ES','052ES','053ES','06RS','061ES','062ES','063ES','07RS','071ES','072ES','073ES','08RS','081ES','082ES','083ES','09RS','091ES','092ES','093ES','10RS','101ES','102ES','103ES','11RS','111ES','112ES','113ES','12RS','121ES','122ES','123ES','13RS','131ES','132ES','133ES','14RS','141ES','142ES','143ES','15RS','151ES','152ES','153ES','16RS','161ES','162ES','163ES','17RS','171ES','172ES','173ES','18RS','181ES','182ES','183ES','19RS','191ES','192ES','193ES','20RS','201ES','202ES','203ES','21RS','211ES','212ES','213ES','22RS','221ES','222ES','223ES']

for year in years:
    yearurl = 'https://www.legis.la.gov/Legis/ActNumbers.aspx?sid=' + year
    try:
        driver.get(yearurl)
        total = driver.find_element_by_css_selector("#ctl00_ctl00_PageBody_PageContent_LabelTotalInstruments").text.split(" Instruments")[0].split("are ")[1]
        total_num = math.ceil(int(total)/100)
        for i in range(0,total_num+1):
            try:
                for i in range(0,100):
                    driver.get(yearurl)
                    element = '#ctl00_ctl00_PageBody_PageContent_ListViewActs_ctrl' + str(i) + '_HyperLink1'
                    driver.find_element_by_css_selector(element).click()
                    url = driver.current_url
                    actpdf_url = "https://www.legis.la.gov/Legis/BillDocs.aspx?i=" +  str(url).split("i=")[1] + "&t=text"
                    driver.get(actpdf_url)
                    driver.find_element_by_css_selector("#formBillDocs > table > tbody > tr:nth-child(1) > td > a").click()
                pages = driver.find_elements_by_css_selector("#ctl00_ctl00_PageBody_PageContent_DataPager1 > a")
                nextpage = "#ctl00_ctl00_PageBody_PageContent_DataPager1 > a:nth-child(" + str(len(pages)) + ")"
                driver.find_element_by_css_selector(nextpage).click()
            except:
                print("skip")
    except:
        print("skip")


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

datasource.drop_duplicates(subset = ['Full text'],
                     keep = 'first', inplace = True, ignore_index= True)

datasource.to_excel('LA_Leginfo.xlsx')
datasource.to_csv('LA_Leginfo.csv')
datasource.to_pickle('LA_Leginfo.pkl')
datasource.to_json('LA_Leginfo.json')

