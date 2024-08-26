#!/usr/bin/env python
# coding: utf-8

# # Ch 7 California

# [California Legislative information](https://leginfo.legislature.ca.gov/faces/advance/advance.xhtml) is an official website that stores all acts passed in California. The web address is https://leginfo.legislature.ca.gov/faces/home.xhtml.
# 
# ![California Legislative information](pics/ca_web.png)

# California Legislative information Website provides [*Advanced Search*](https://leginfo.legislature.ca.gov/faces/advance/advance.xhtml) function. Through selecting all sessions as shown below, we can get all bills information available on the website. Under the column *Status*, we can tell which bill is chaptered, i.e.,becoming a law. Then, the task of webscraping is to extract the information of all chaptered bills on the website.
# 
# ![California Legislative information](pics/ca_search.png)

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


# ## Direct webscraping
# As shown on [California Legislative information Website](https://leginfo.legislature.ca.gov/faces/advance/advance.xhtml) after searching all sessions, we can see returned bills one by one. Clicking the bill under column *Measure*, there is the full text of the bill. For efficiency purposes, we first get all urls for chaptered bills and extract the full texts of the chaptered bills after clicking each url.
# ### Get all urls

# In[ ]:


sessions = ['2021 - 2022', '2019 - 2020', '2017 - 2018', '2015 - 2016', '2013 - 2014', '2011 - 2012', '2009 - 2010', '2007 - 2008', '2005 - 2006', '2003 - 2004', '2001 - 2002', '1999 - 2000']

urls = []
measures = []
subjects = []
authors = []
statuss = []

for session in sessions:
    print(session)
    driver.get("https://leginfo.legislature.ca.gov/faces/billSearchClient.xhtml")
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#attrSearch"))
    )
    select_session = Select(driver.find_element_by_css_selector('select#session_year'))
    select_session.select_by_visible_text(session)
    search = driver.find_element_by_css_selector('#attrSearch')
    search.click()

    WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.CSS_SELECTOR, "tbody tr")))
    bills = driver.find_elements_by_css_selector('tbody tr')
    for bill in bills:
        if bill.find_element_by_css_selector("td:nth-child(4)").text == 'Chaptered':
           url = bill.find_element_by_css_selector("td:nth-child(1) a").get_attribute('href')
           urls.append(url)
           measure = bill.find_element_by_css_selector("td:nth-child(1) a").text
           measures.append(measure)
           subject = bill.find_element_by_css_selector("td:nth-child(2)").text
           subjects.append(subject)
           author = bill.find_element_by_css_selector("td:nth-child(3)").text
           authors.append(author)
           status = bill.find_element_by_css_selector("td:nth-child(4)").text
           statuss.append(status)
        else:
           print("Bill Died")
        time.sleep(0.01)
print("url done")


# ### Extract full texts
# With the urls we scraped from last subsection, we click each url and extract the full bill text.

# In[ ]:


for url in urls:
    driver.get(url)
    state = "CA"
    states.append(state)

    billnumber = driver.find_element_by_css_selector('#bill_header > div:nth-child(3) > h1')
    billnumbers.append(billnumber.text.rsplit(" ")[0])

    title = driver.find_element_by_css_selector('#bill_header > div:nth-child(3) > h1')
    title = title.text.split(" ",1)[1]
    titles.append((title.rsplit("(",1)[0]))

    textlinks.append(url)
    fulltext = driver.find_element_by_css_selector("#bill_all").text
    fulltexts.append(fulltext)
    fulltextpage = driver.find_element_by_css_selector("#centercolumn").text
    fulltextpages.append(fulltextpage)
    sleeptime = randint(1,11)*0.1
    time.sleep(sleeptime)


# ## Text saving and output
# 
# After webscraping all chaptered bills' full texts, we saved them into different formats of files.

# In[ ]:


datasource = pd.DataFrame({
    'Year': years,
    'State': states,
    'Session Year': sessionyears,
    'Bill Number': billnumbers,
    'Name': titles,
    'Brief Summary': briefsummarys,
    'Introduced Date': introduceddates,
    'Date it was signed':signingdates,
    'Date effective':effectivedates,
    'Expiration date':expireddates,
    'Introducer':leadauthors,
    'Full text': fulltexts,
    'Link to full text':textlinks
})

# save bill info into files
datasource.to_excel('CA_Leginfo.xlsx')
datasource.to_csv('CA_Leginfo.csv')
datasource.to_pickle('CA_Leginfo.pkl')
datasource.to_json('CA_Leginfo.json')

