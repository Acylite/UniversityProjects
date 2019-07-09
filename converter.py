import sys
import csv
import json
import pandas as pd
import re
import framework
from urllib.error import URLError, HTTPError

dbase = framework.Framework()
content = dbase.content

class Converter():
    final = dbase.final
    #open in json format
    
    def json(arg, headers, c, bigC, self):
        
        returnh = []
        
        response = framework.requests.get(self)
            
        soup = framework.BeautifulSoup(response.text, "html.parser")
    
        targetURL = soup.find('a',{"alt":"API URL"})["href"]
        for attempt in range(1,10):
            try:
                print("searching URL: " + targetURL)
                response = framework.urllib.request.urlopen(targetURL)
            except HTTPError as e:
                if attempt < 9:
                    print('The server couldn\'t fulfill the request.')
                    print('Reconnecting Attempt: ' + str(attempt))
                    continue
                else:
                    raise
            except URLError as e:
                if attempt < 9:
                    print('We failed to reach a server.')
                    print('Reconnecting Attempt: ' + str(attempt))
                    continue
                else:
                    raise
            else:
                print("connected to URL")
                response = response.read()
            
                header = soup.findAll('table', {'border': '1'})
                header = header[len(header)-1].findAll('td')
            
                iterable = iter(range(1,len(header)+1))
             
                for i in iterable:
                     if i % 4 == 0:
                        header[i-1] = str(header[i-1])
                        header[i-1] = header[i-1].replace('&amp;', 'and')
                        header[i-1] = header[i-1].replace('</td>', '')
                        header[i-1] = header[i-1].replace('<td>', '')
                        header[i-1] = header[i-1].replace('<br/>', ' ')
                        header[i-1] = re.sub(re.compile('<sup>.*?</sup>'),"",header[i-1])
                        returnh.append(header[i-1])
                headers.append(returnh)
                bigC.append(c)
            break
        j = json.loads(response)
        r = json.dumps(j).replace('null', '"NA"')
        response = json.loads(r)
        return(response)
              
    #converts list of URLS to json list
        
    def divide(arg, headers, bigC, self):
        c = 0
        idx0 = 0
        idxn = len(self[0])-1
        midval = (idx0 + idxn)// 2
        percentage = 0.0
        while idx0 <= midval:
            percentage += 1/len(self[0])*100
            self[0][idx0] = Converter().json(headers, c, bigC, self[0][idx0])
            print(str(int(percentage)) + "% complete")
            c += 1
            idx0 = idx0 + 1
            
            if midval < idxn:
                percentage += 1/len(self[0])*100
                self[0][idxn] = Converter().json(headers, c,bigC, self[0][idxn])
                print(str(int(percentage)) + "% complete")
                c += 1
                idxn = idxn - 1
            


    def writer(arg, self):
        print("Converting Section " + str(self))
        tablenum = self
        bigC = []
        self = Converter().final[self-1]
        headers = []
        Converter().divide(headers, bigC, self)
        
        #create the csv writer object
       
        writer = pd.ExcelWriter('C:/HKMA_data_ALL/HKMA section ' + str(self[1]) +'.xlsx', engine = 'xlsxwriter')
        json_parsed = []
        idx0 = 0 
        idxn = len(self[0])-1
        midval = (idx0 + idxn)// 2
        b = 0
        while idx0 <= midval:
            tempjson = self[0][idx0]
            col = list(tempjson['result']['records'][0].keys())
            tempjson = pd.DataFrame(tempjson['result']['records'])
            tempjson = tempjson.reindex(col, axis = 1)
            tempjson.columns = headers[b]
            tempjson = tempjson.sort_values(tempjson.columns[0], ascending = True)
            json_parsed.append(tempjson)
            b += 1
            idx0 = idx0 + 1
            if midval < idxn:
                tempjson = self[0][idxn]
                col = list(tempjson['result']['records'][0].keys())
                tempjson = pd.DataFrame(tempjson['result']['records'])
                tempjson = tempjson.reindex(col, axis = 1)
                tempjson.columns = headers[b]
                print("headers " + str(headers[b]))
                tempjson = tempjson.sort_values(tempjson.columns[0], ascending = True)
                json_parsed.append(tempjson)
                b += 1
                idxn = idxn - 1
        tmp = [i for i in content if i.startswith('Table ' + str(self[1]))]
        c = 0
        id0 = 0
        print("contents in table " + str(tablenum))
        while id0 < len(json_parsed):
            if len(str(tmp[bigC[c]])) < 31:
                maxlen = len(str(tmp[bigC[c]]))
            else:
                maxlen = 30
            json_parsed[id0].to_excel(writer, sheet_name = str(tmp[bigC[c]])[0:maxlen])
            print(str(tmp[bigC[c]]))
            id0 = id0 + 2
            c += 1 
        if len(json_parsed) % 2 == 0:
            id0 = id0 - 1
        else:
            id0 = id0 - 3
        while id0 > 0:
            if len(str(tmp[bigC[c]])) < 31:
                maxlen = len(str(tmp[bigC[c]]))
            else:
                maxlen = 30
            json_parsed[id0].to_excel(writer, sheet_name = str(tmp[bigC[c]])[0:maxlen])
            print(str(tmp[bigC[c]]))
            id0 -= 2
            c += 1
        writer.save()
        print("Table " + str(self[1]) + " complete")

    
    
