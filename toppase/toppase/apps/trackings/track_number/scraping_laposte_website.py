# -*- coding: utf8 -*-
import requests
from bs4 import BeautifulSoup
import json
import interpreter_dict_Laposte
import datetime
from unidecode import unidecode


def interprete(content):
    return interpreter_dict_Laposte.status_dict[content]


def track_laposte(track_number):
    table_field = ["date", "status", "location",]
    url = "https://www.laposte.fr/particulier/outils/en/track-a-parcel?code="+str(track_number)
    req = requests.get(url)
    html = BeautifulSoup(req.text, "html.parser")
    content_tag = html.find("table")
    rows = content_tag.find_all('tr')
    table_json = []

    first_loop = 0
    i=0
    for tr in rows:
        i+=1
        cols = tr.find_all('td')
        temp = {"date": "", "status": "", "location": ""}
        count = 0
        if first_loop==0:
            first_loop = 1
            continue
        estimation_date=''
        for td in cols:
            for tag in td.find_all("a"):
                tag.replace_with('')
            content = td.get_text()
            if count == 1:
                content = interprete(content)
            elif count==0 :
                if i==len(rows):
                    estimation_date = datetime.datetime.strptime(str(content), "%m/%d/%Y")+datetime.timedelta(days=2)
            temp[table_field[count]]= content
            # print "<p>%s</p>"%content
            count += 1
        table_json.append(temp)
        # print '-----------------------------------------'
        json_laposte={}
        json_laposte["scan_event_list"]=table_json
        json_laposte["estimated_date"] = str(estimation_date)
        json_laposte["shipper"] ="laposte"

    return json.dumps(json_laposte)

# track_laposte("11111111111")


