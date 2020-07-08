# -*- coding: utf-8 -*-

"""
@author: Gaspard
"""

import requests
import re, csv,json
from bs4 import BeautifulSoup

bibURL= "https://bibliotheques.paris.fr/Default/search.aspx"

headers = {'User-Agent': 'Mozilla/5.0'}
r1 = requests.get("https://bibliotheques.paris.fr/Default/search.aspx",
                  headers=headers)
print(r1.status_code, r1.reason)

r2 = requests.post("https://bibliotheques.paris.fr/Default/Portal/Recherche/OpenFind.svc/GetLightSelection",
                   data="")
print(r2.status_code, r2.reason)
print(r2.text)


data = {
    "query": {
        "Page":0,
        "PageRange":3,
        "QueryString":"thorgal",
        "ResultSize":"100",
        "ScenarioCode":"DEFAULT",
        "SearchContext":0,
        "SearchLabel":"",
    }
}
r3 = requests.post("https://bibliotheques.paris.fr/Default/Portal/Recherche/Search.svc/Search",json=data)
print(r3.status_code, r3.reason)
bs = BeautifulSoup(r3.text)

a['d']['Results']



data = {
    "Record":
    {
        "RscId":"1232233",
        "Docbase":"SYRACUSE",
        "PazPar2Id":"0_OFFSET_0"
    },
    "searchQuery":
    {
        "FacetFilter":"{}",
        "ForceSearch":false,
        "Page":0,
        "PageRange":3,
        "QueryGuid":"a65886fc-1313-4427-8984-860fe533ba68",
        "QueryString":"*:*",
        "ResultSize":20,
        "ScenarioCode":"DEFAULT",
        "ScenarioDisplayMode":"display-standard",
        "SearchLabel":"",
        "SearchTerms":"",
        "SortField":null,
        "SortOrder":0,
        "TemplateParams":
        {
            "Scenario":"",
            "Scope":"Default",
            "Size":null,
            "Source":"",
            "Support":""
        },
        "UseSpellChecking":null
    }
}
r4 = requests.post("https://bibliotheques.paris.fr/Default/Portal/Services/ILSClient.svc/GetHoldings",json=data)
print(r4.status_code, r4.reason)
bs4 = BeautifulSoup(r4.text)

a['d']['Results'][0]
