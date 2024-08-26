#!/usr/bin/env python
# coding: utf-8

# # Ch 9 Connecticut

# In[ ]:


# import libraries
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
import fitz
import time

# driver_path = r'C:\Users\longy\OneDrive\Projects\AFRI\windows\chromedriver.exe' #for windows
driver_path = '/Users/long/OneDrive/Projects/AFRI/chromedriver'
# driver = webdriver.Chrome(executable_path=DRIVER_PATH)

# Change the working directory
os.chdir('/Volumes/GoogleDrive/Shared drives/UCSC-UMN AFRI project/Data/Raw_Data/CT/')
# os.chdir('C:/Users/longy/OneDrive/Projects/AFRI/')
# Get the current working directory
cwd = os.getcwd()
# Print the current working directory
print("Current working directory: {0}".format(cwd))

acttxts = []
path = "/Volumes/GoogleDrive/Shared drives/UCSC-UMN AFRI project/Data/Raw_Data/CT"
files = glob.glob(os.path.join(path, '*.pdf'))
files.extend(glob.glob(os.path.join(path, '*.PDF')))
for file in files:
    doc = fitz.open(file)
    pgtxts = []
    for page in doc:
        pgtxt = page.get_text()
        pgtxts.append(pgtxt)
        acttxt = ' '.join(pgtxts)
    acttxts.append(acttxt)
    doc.close()

datasource = pd.DataFrame({
    #'Link to full text':session_urls,
    'Full text': acttxts
})

datasource.to_excel('CT_Leginfo.xlsx')
datasource.to_csv('CT_Leginfo.csv')
datasource.to_pickle('CT_Leginfo.pkl')
datasource.to_json('CT_Leginfo.json')

