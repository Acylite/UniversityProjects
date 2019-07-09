#framework.py
import requests
import xlsxwriter
import urllib.request
import re
from bs4 import BeautifulSoup
    
class Framework():
    import os
    if not os.path.exists('C:/HKMA_data_ALL'):
        os.makedirs('C:/HKMA_data_ALL')
    url = "https://www.hkma.gov.hk/eng/market-data-and-statistics/monthly-statistical-bulletin/table.shtml"
    response=  requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    counter = 0
    tnum = []
    tables = {}
    content = {}
    tablenum = 1
    bigtable = []
    sectionMax = soup.findAll('a', {'class':'anchorLink'})
    sectionMax = sectionMax[len(sectionMax)-1]['name']
    sectionMax = sectionMax.replace('section', '')
    sectionMax = int(sectionMax)
    for i in range(1,sectionMax+1):
        tables["table" + str(i)] = []
        content["table" + str(i)] = []
    for table in tables:
        table = soup.findAll('a', title = re.compile("Table " + str(tablenum)+"."))
        bigtable.append(table)
        temp = []
        for i in table:
            temp.append(counter)               
            counter += 1
        if tablenum == 3:
            counter -= 1
            temp.remove(counter)
        tnum.append(temp)
        tablenum += 1
    API = soup.findAll('a',  text = "API")
   
    
    #header = soup.findAll('table', {'border': '1'})
    
    content = []
    for i in range(0, len(bigtable)):
        for j in range(0, len(bigtable[i])):
            s1 = bigtable[i][j]['title']
            s2 = "DownloadÂ"
            content.append(s1[s1.index(s2) + len(s2) + 1:])
   
    tablei = 1
    for t in tnum:
        temp = []
        for j in t: 
            temp.append(API[j]['href'])
        tables['table' + str(tablei)] = temp
        tablei += 1
    
    final = []
    for i in range(1, sectionMax+1):
        temp = [] 
        for j in tables['table'+str(i)]:
            temp.append(j)
        final.append([temp , i])
    
    #retrieves the headers
