#!/usr/bin/env python
# coding: utf-8

# # Ch 1 Webscraping tool setup

# In this chapter, we introduce the webscraping tool set.
# 
# ## Python Language
# 
# Python is a programming language that lets you work more quickly and integrate your systems more effectively (https://www.python.org/).
# 
# ## IDEs
# 
# An IDE (Integrated Development Environment) understand your code much better than a text editor. It usually provides features such as build automation, code linting, testing and debugging. This can significantly speed up your work. The downside is that IDEs can be complicated to use. There are several IDEs that users can consider. Here we recommend

# 
# ## Libraries
# 
# A Python library, like packages in R, is a reusable chunk of code to save time. Several useful libraries are needed to install for Python to run this script.
# 
# Selenium is a powerful web scraping tool by automating browsers to load the target website, retrieve the required data, and take screenshots or assert that certain actions happen on the website. This script relies heavily on Selenium. In addition to Selenium, we also need to import other necessary packages such as pandas,time, os, PyPDF2, glob, pick

# In[ ]:


# import libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
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

