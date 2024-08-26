#!/usr/bin/env python
# coding: utf-8

# # Ch 7 California

# 

# In[ ]:


sessions = ['2021 - 2022', '2019 - 2020', '2017 - 2018', '2015 - 2016', '2013 - 2014', '2011 - 2012', '2009 - 2010',
            '2007 - 2008', '2005 - 2006', '2003 - 2004', '2001 - 2002', '1999 - 2000']

urls = []
measures = []
subjects = []
authors = []
statuss = []
subjects1 = []
authors1 = []
statuss1 = []
# search bills by iterating sessionyears first and then keywords
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
            print("Do not pass")
        time.sleep(0.01)
print("url done")

# set up list titles
years = []
states = []
sessionyears = []
billnumbers = []
titles = []
briefsummarys = []
introduceddates = []
signingdates = []
effectivedates = []
expireddates = []
leadauthors = []
textlinks = []
fulltexts = []
fulltextpages = []

# extract bill information on each bill

for url in urls[6313:]:
    driver.get(url)
    state = "CA"
    states.append(state)

    billnumber = driver.find_element_by_css_selector('#bill_header > div:nth-child(3) > h1')
    billnumbers.append(billnumber.text.rsplit(" ")[0])

    title = driver.find_element_by_css_selector('#bill_header > div:nth-child(3) > h1')
    title = title.text.split(" ", 1)[1]
    titles.append((title.rsplit("(", 1)[0]))

    textlinks.append(url)
    fulltext = driver.find_element_by_css_selector("#bill_all").text
    fulltexts.append(fulltext)
    fulltextpage = driver.find_element_by_css_selector("#centercolumn").text
    fulltextpages.append(fulltextpage)
    sleeptime = randint(1, 11) * 0.1
    time.sleep(sleeptime)

datasource = pd.DataFrame({
    'Year': years,
    'State': states,
    'Session Year': sessionyears,
    'Bill Number': billnumbers,
    'Name': titles,
    'Brief Summary': briefsummarys,
    'Introduced Date': introduceddates,
    'Date it was signed': signingdates,
    'Date effective': effectivedates,
    'Expiration date': expireddates,
    'Introducer': leadauthors,
    'Full text': fulltexts,
    'Link to full text': textlinks
})

datasource = pd.DataFrame({
    'Year': years,
    'State': states,
    'Session Year': sessionyears,
    'Bill Number': billnumbers,
    'Name': titles,
    'authors': authors,
    'Brief Summary': briefsummarys,
    'Introduced Date': introduceddates,
    'Date effective': effectivedates,
    'Expiration date': expireddates,
    'Full text': fulltexts,
    'Link to full text': textlinks
})

# Python program to read
# json file


# Opening JSON file

os.chdir('/Volumes/GoogleDrive/Shared drives/UCSC-UMN AFRI project/Data/CA/')
f = open('CA_Leginfo.json')
# os.chdir('/Volumes/GoogleDrive/Shared drives/UCSC-UMN AFRI project/Data/GA')
# Get the current working directory
cwd = os.getcwd()
# Print the current working directory
print("Current working directory: {0}".format(cwd))

#datasource = json.load(f)

#datasource = pd.read_pickle("CA_Leginfo.pkl")
#datasource = datasource.drop(['authors','Introduced Date','Date effective','Expiration date'], axis = 1)

# save bill info into files
datasource.to_excel('CA_Leginfo.xlsx')
datasource.to_csv('CA_Leginfo.csv')
from sqlalchemy import create_engine

engine = create_engine('sqlite://', echo=False)
datasource.to_sql('CA_Leginfo.sql', con=engine)
datasource.to_pickle('CA_Leginfo.pkl')
datasource.to_json('CA_Leginfo.json')

datasource.to_stata('CA_Leginfo.dta')

print("download finished")


# In[ ]:


sessions = ['2021 - 2022', '2019 - 2020', '2017 - 2018', '2015 - 2016', '2013 - 2014', '2011 - 2012', '2009 - 2010',
            '2007 - 2008', '2005 - 2006', '2003 - 2004', '2001 - 2002', '1999 - 2000']

urls = []
measures = []
subjects = []
authors = []
statuss = []
subjects1 = []
authors1 = []
statuss1 = []
# search bills by iterating sessionyears first and then keywords
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
            print("Do not pass")
        time.sleep(0.01)
print("url done")

# set up list titles
years = []
states = []
sessionyears = []
billnumbers = []
titles = []
briefsummarys = []
introduceddates = []
signingdates = []
effectivedates = []
expireddates = []
leadauthors = []
textlinks = []
fulltexts = []
fulltextpages = []

# extract bill information on each bill

for url in urls[6313:]:
    driver.get(url)
    state = "CA"
    states.append(state)

    billnumber = driver.find_element_by_css_selector('#bill_header > div:nth-child(3) > h1')
    billnumbers.append(billnumber.text.rsplit(" ")[0])

    title = driver.find_element_by_css_selector('#bill_header > div:nth-child(3) > h1')
    title = title.text.split(" ", 1)[1]
    titles.append((title.rsplit("(", 1)[0]))

    textlinks.append(url)
    fulltext = driver.find_element_by_css_selector("#bill_all").text
    fulltexts.append(fulltext)
    fulltextpage = driver.find_element_by_css_selector("#centercolumn").text
    fulltextpages.append(fulltextpage)
    sleeptime = randint(1, 11) * 0.1
    time.sleep(sleeptime)

datasource = pd.DataFrame({
    'Year': years,
    'State': states,
    'Session Year': sessionyears,
    'Bill Number': billnumbers,
    'Name': titles,
    'Brief Summary': briefsummarys,
    'Introduced Date': introduceddates,
    'Date it was signed': signingdates,
    'Date effective': effectivedates,
    'Expiration date': expireddates,
    'Introducer': leadauthors,
    'Full text': fulltexts,
    'Link to full text': textlinks
})

datasource = pd.DataFrame({
    'Year': years,
    'State': states,
    'Session Year': sessionyears,
    'Bill Number': billnumbers,
    'Name': titles,
    'authors': authors,
    'Brief Summary': briefsummarys,
    'Introduced Date': introduceddates,
    'Date effective': effectivedates,
    'Expiration date': expireddates,
    'Full text': fulltexts,
    'Link to full text': textlinks
})

# Python program to read
# json file


# Opening JSON file

os.chdir('/Volumes/GoogleDrive/Shared drives/UCSC-UMN AFRI project/Data/CA/')
f = open('CA_Leginfo.json')
# os.chdir('/Volumes/GoogleDrive/Shared drives/UCSC-UMN AFRI project/Data/GA')
# Get the current working directory
cwd = os.getcwd()
# Print the current working directory
print("Current working directory: {0}".format(cwd))

#datasource = json.load(f)

#datasource = pd.read_pickle("CA_Leginfo.pkl")
#datasource = datasource.drop(['authors','Introduced Date','Date effective','Expiration date'], axis = 1)

# save bill info into files
datasource.to_excel('CA_Leginfo.xlsx')
datasource.to_csv('CA_Leginfo.csv')
from sqlalchemy import create_engine

engine = create_engine('sqlite://', echo=False)
datasource.to_sql('CA_Leginfo.sql', con=engine)
datasource.to_pickle('CA_Leginfo.pkl')
datasource.to_json('CA_Leginfo.json')

datasource.to_stata('CA_Leginfo.dta')

print("download finished")


# In[ ]:


driver.get("http://alisondb.legislature.state.al.us/alison/SelectSession.aspx")


# There are three types of law sessions including regular session, special session and special organization session. All enrolled bills are named by "HB","SB","SR","HR","SJR", or "HJR" plus bill number and ended with "-enr". They are stored as pdf files on Alabama Secretary of State website. You can check the bills on https://arc-sos.state.al.us/CGI/actyear.mbr/input.

# In[ ]:


sessions = ['2021 - 2022', '2019 - 2020', '2017 - 2018', '2015 - 2016', '2013 - 2014', '2011 - 2012', '2009 - 2010',
            '2007 - 2008', '2005 - 2006', '2003 - 2004', '2001 - 2002', '1999 - 2000']

urls = []
measures = []
subjects = []
authors = []
statuss = []
subjects1 = []
authors1 = []
statuss1 = []
# search bills by iterating sessionyears first and then keywords
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
            print("Do not pass")
        time.sleep(0.01)
print("url done")

# set up list titles
years = []
states = []
sessionyears = []
billnumbers = []
titles = []
briefsummarys = []
introduceddates = []
signingdates = []
effectivedates = []
expireddates = []
leadauthors = []
textlinks = []
fulltexts = []
fulltextpages = []

# extract bill information on each bill

for url in urls[6313:]:
    driver.get(url)
    state = "CA"
    states.append(state)

    billnumber = driver.find_element_by_css_selector('#bill_header > div:nth-child(3) > h1')
    billnumbers.append(billnumber.text.rsplit(" ")[0])

    title = driver.find_element_by_css_selector('#bill_header > div:nth-child(3) > h1')
    title = title.text.split(" ", 1)[1]
    titles.append((title.rsplit("(", 1)[0]))

    textlinks.append(url)
    fulltext = driver.find_element_by_css_selector("#bill_all").text
    fulltexts.append(fulltext)
    fulltextpage = driver.find_element_by_css_selector("#centercolumn").text
    fulltextpages.append(fulltextpage)
    sleeptime = randint(1, 11) * 0.1
    time.sleep(sleeptime)

datasource = pd.DataFrame({
    'Year': years,
    'State': states,
    'Session Year': sessionyears,
    'Bill Number': billnumbers,
    'Name': titles,
    'Brief Summary': briefsummarys,
    'Introduced Date': introduceddates,
    'Date it was signed': signingdates,
    'Date effective': effectivedates,
    'Expiration date': expireddates,
    'Introducer': leadauthors,
    'Full text': fulltexts,
    'Link to full text': textlinks
})

datasource = pd.DataFrame({
    'Year': years,
    'State': states,
    'Session Year': sessionyears,
    'Bill Number': billnumbers,
    'Name': titles,
    'authors': authors,
    'Brief Summary': briefsummarys,
    'Introduced Date': introduceddates,
    'Date effective': effectivedates,
    'Expiration date': expireddates,
    'Full text': fulltexts,
    'Link to full text': textlinks
})

# Python program to read
# json file


# Opening JSON file

os.chdir('/Volumes/GoogleDrive/Shared drives/UCSC-UMN AFRI project/Data/CA/')
f = open('CA_Leginfo.json')
# os.chdir('/Volumes/GoogleDrive/Shared drives/UCSC-UMN AFRI project/Data/GA')
# Get the current working directory
cwd = os.getcwd()
# Print the current working directory
print("Current working directory: {0}".format(cwd))

#datasource = json.load(f)

#datasource = pd.read_pickle("CA_Leginfo.pkl")
#datasource = datasource.drop(['authors','Introduced Date','Date effective','Expiration date'], axis = 1)

# save bill info into files
datasource.to_excel('CA_Leginfo.xlsx')
datasource.to_csv('CA_Leginfo.csv')
from sqlalchemy import create_engine

engine = create_engine('sqlite://', echo=False)
datasource.to_sql('CA_Leginfo.sql', con=engine)
datasource.to_pickle('CA_Leginfo.pkl')
datasource.to_json('CA_Leginfo.json')

datasource.to_stata('CA_Leginfo.dta')

print("download finished")

