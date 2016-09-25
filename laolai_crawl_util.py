# -*- coding: utf-8 -*-
import urllib    
import urllib2  
import math
import time 
import json
from bs4 import BeautifulSoup
from collections import OrderedDict

history = []
def pageClean(raw):
    return (raw.split('(', 1)[1])[:-2]

def pageProcess(raw):
    item_list = []
    c = pageClean(raw)
    jc = json.loads(c)
    queryRet = jc['data'][0]['result']
    nor = len(queryRet)
    for item in queryRet:
        #ignore the repeated records
        if item['loc'] not in history:
            item_list.append(item)
            history.append(item['loc'])
    return (item_list,nor)

def genGetRequest(name,pn,rn):
    t = int(round(time.time() * 1000))
    # need to keep the order 
    values = OrderedDict()
    values["resource_id"]=6899
    values["query"]="失信被执行人名单"
    values["cardNum"]=""
    values["iname"]=name
    values["areaName"]=""
    values["pn"] = pn
    values["rn"] = rn
    values["ie"]="utf-8"
    values["oe"]="utf-8"
    values["format"]="json"
    values["t"]=t
    values["cb"]="jQuery1102019526977392588996_"+str(time)
    values["_"]=t
    url = "http://opendata.baidu.com/api.php"
    data = urllib.urlencode(values) 
    geturl = url + "?"+data
    request = urllib2.Request(geturl)
    return request

def getResponse(request):
    return urllib2.urlopen(request)

def crawler_exe(_username,_output):
    final_list = []
    #example url = "http://opendata.baidu.com/api.php?resource_id=6899&query=%E5%A4%B1%E4%BF%A1%E8%A2%AB%E6%89%A7%E8%A1%8C%E4%BA%BA%E5%90%8D%E5%8D%95&cardNum=&iname=%E7%8E%8B%E6%96%87%E6%9E%97&areaName=%E5%B1%B1%E4%B8%9C&ie=utf-8&oe=utf-8&format=json&t=1474752903379&cb=jQuery110209960325513495023_1474750703993&_=1474750704031"
    name = _username
    output = _output

    pn = 0  #start record
    rn = 10 #10 records per page
    lastNum = 11
    print "crawling user ",name
    while lastNum >10:
        request = genGetRequest(name,pn,rn)
        response = getResponse(request)
        soup = BeautifulSoup(response,"lxml")
        content = soup.find('p').get_text().encode("utf-8")
        singlePageRet = pageProcess(content)
        pn = pn+10
        lastNum = singlePageRet[1]
        final_list.extend(singlePageRet[0])

        #print str(len(final_list))+" on page: "+str(pn)+" last number: "+str(lastNum)
    json.dump(final_list,output,indent=2)

