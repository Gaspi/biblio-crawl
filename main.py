# -*- coding: utf-8 -*-

import requests

bib   = "https://bibliotheques.paris.fr/"

r1 = requests.get(bib+"Default/search.aspx")
print(r1.status_code, r1.reason)

def search(s):
    data = {
        "query": {
            "Page":0,
            "PageRange":3,
            "QueryString":s,
            "ResultSize":100,
            "ScenarioCode":"DEFAULT",
            "SearchContext":0,
            "SearchLabel":"",
        }
    }
    r3 = requests.post(bib+"Default/Portal/Recherche/Search.svc/Search",json=data)
    print(r3.status_code, r3.reason)

    search = r3.json()
    for r in search['d']['Results']:
        print(r['Resource']['RscId'],r['Resource']['Ttl'])
    res = search['d']['Results'][0]['Resource']
    print(search['d']['Results'][1]['Resource'])

    data = {  "Record":{ "RscId":res['RscId'], "Docbase":"SYRACUSE", "PazPar2Id":"0_OFFSET_0"}  }
    r4 = requests.post(bib+"Default/Portal/Services/ILSClient.svc/GetHoldings",json=data)
    print(r4.status_code, r4.reason)

    a = r4.json()

    for e in a['d']['Holdings']:
        if e['Statut'] == 'En rayon':
            print(e['Site'])


search('thorgal+tome+01')

