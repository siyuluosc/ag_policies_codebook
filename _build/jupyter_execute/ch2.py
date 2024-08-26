#!/usr/bin/env python
# coding: utf-8

# # Ch 2 Webscraping Targets and Strategies

# Our goal is to webscrape all session laws during 1975-2022 from state-level legislature websites. The General and Special Laws of Texas, often referred to as the "session laws," constitute a complete set of all bills passed into law by each session of the state legislature.Session laws are organized into chapters, with each chapter consisting of a single "Act," or bill. As bills are passed into law during a legislative session, the Secretary of State assigns each Act a corresponding chapter number.

# | Name	    | FIPS State Numeric Code	  |Official USPS Code	| Website Address|
# |----------|---------------------------|---------------------:|------------------------------:|
# |Alabama|1|AL|https://arc-sos.state.al.us/CGI/actyear.mbr/input|
# |Alaska|2|AK|http://www.akleg.gov/basis/Home/BillsandLaws|
# |Arizona|4|AZ|https://apps.azleg.gov/BillStatus/BillOverview?Sessionid=123|
# |Arkansas|5|AR|https://www.arkleg.state.ar.us/Acts/|
# |California|6|CA|https://leginfo.legislature.ca.gov/faces/home.xhtml|
# |Colorado|8|CO|https://leg.colorado.gov/bills|
# |Connecticut|9|CT|https://www.cga.ct.gov/asp/menu/legdownload.asp|
# |Delaware|10|DE|https://legis.delaware.gov/AllLegislation|
# |District of Columbia|11|DC|https://lims.dccouncil.us/searchresult/|
# |Florida|12|FL|http://www.leg.state.fl.us/Welcome/index.cfm|
# |Georgia|13|GA|https://www.legis.ga.gov/legislation/all|
# |Hawaii|15|HI|https://www.capitol.hawaii.gov/|
# |Idaho|16|ID|https://legislature.idaho.gov/statutesrules/sessionlaws/|
# |Illinois|17|IL|https://www.ilga.gov/previousga.asp|
# |Indiana|18|IN|http://iga.in.gov/results/#|
# |Iowa|19|IA|https://www.legis.iowa.gov/legislation/billTracking|
# |Kansas|20|KS|http://www.kslegislature.org/li/historical/|
# |Kentucky|21|KY|https://legislature.ky.gov/Law/Pages/KyActs.aspx|
# |Louisiana|22|LA|https://www.legis.la.gov/Legis/SessionInfo/SessionInfo.aspx|
# |Maine|23|ME|https://legislature.maine.gov/ros/LOM/LOMpdfDirectory.htm|
# |Maryland|24|MD|http://mgaleg.maryland.gov/mgawebsite/Search/FullText|
# |Massachusetts|25|MA|https://malegislature.gov/Laws/SessionLaws|
# |Michigan|26|MI|https://www.legislature.mi.gov/|
# |Minnesota|27|MN|https://www.revisor.mn.gov/search/?search=stat|
# |Mississippi|28|MS|http://billstatus.ls.state.ms.us/sessions.htm|
# |Missouri|29|MO|https://house.mo.gov/LegislationSP.aspx?focusedID=Bill%20List|
# |Montana|30|MT|http://laws.leg.mt.gov/legprd/law0203w$.startup?P_SESS=19991|
# |Nebraska|31|NE|https://nebraskalegislature.gov/laws/laws.php|
# |Nevada|32|NV|https://www.leg.state.nv.us/Site/Search/search.cfm|
# |New Hampshire|33|NH|http://www.gencourt.state.nh.us/bill_status/legacy/bs2016/|
# |New Jersey|34|NJ|https://www.njleg.state.nj.us/bills/Bills_ADVS.aspx#|
# |New Mexico|35|NM|https://www.nmlegis.gov/Search|
# |New York|36|NY|https://nyassembly.gov/leg/?sh=advanced|
# |North Carolina|37|NC|https://www.ncleg.gov/Search/BillText/|
# |North Dakota|38|ND|https://www.legis.nd.gov/search|
# |Ohio|39|OH|https://www.legislature.ohio.gov/legislation/search/|
# |Oklahoma|40|OK|http://www.oklegislature.gov/AdvancedSearchForm.aspx|
# |Oregon|41|OR|https://www.oregonlegislature.gov/bills_laws/Pages/Oregon-Laws.aspx|
# |Pennsylvania|42|PA|https://www.legis.state.pa.us/cfdocs/legis/home/bills/|
# |Rhode Island|44|RI|http://webserver.rilegislature.gov/search/|
# |South Carolina|45|SC|https://www.scstatehouse.gov/query.php|
# |South Dakota|46|SD|https://sdlegislature.gov/Statutes/Archived|
# |Tennessee|47|TN|https://www.capitol.tn.gov/legislation/archives.html|
# |Texas|48|TX|https://lrl.texas.gov/legis/billsearch/lrlhome.cfm|
# |Utah|49|UT|https://le.utah.gov/asp/passedbills/passedbills.asp|
# |Vermont|50|VT|https://legislature.vermont.gov/bill/search/2022|
# |Virginia|51|VA|https://lis.virginia.gov/cgi-bin/legp604.exe?941+men+BIL|
# |Washington|53|WA|http://search.leg.wa.gov/search.aspx#document|
# |West Virginia|54|WV|https://www.wvlegislature.gov/Bill_Status/bill_status.cfm|
# |Wisconsin|55|WI|https://docs.legis.wisconsin.gov/search|
# |Wyoming|56|WY|https://www.wyoleg.gov/Legislation/archives|

# Since each state-level legislature website has different website structure, we adopted three different webscraping strategies: (i) direct webscraping, (ii) downloading act PDF files and extraction, and (iii) mixing them.
# 
# ## Direct Webscraping
# 
# Some legislature websites store acts on their websites as html files or PDF files. So, we can webscrape acts' full texts directly.
# 
# ![](pics/ca.png)

# In[ ]:


$ Direct Webscraping Roadmap
├── Go to the website
├── Find the act full text
├── Save the text


# ## Downloading act PDF files and extraction
# 
# For some legislature websites with acts stored as PDF files, we adopted the strategy to download all act PDF files and extract full texts from PDF files. See [link]https://www.arkleg.state.ar.us/Acts/SearchByRange.
# 

# In[ ]:


$ Downloading act PDF files and extraction roadmap
├── Go to the website
├── Download act PDF files
├── Extract acts from PDF files


# ![](pics/ar_pdf.png)
