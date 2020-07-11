# -*- coding: utf-8 -*-

import requests

bib   = "https://bibliotheques.paris.fr/"

def get_book_infos(b):
    return {'RscId' : b['Resource']['RscId'],
            'Ttl'   : b['Resource']['Ttl'] }

def search_book(search_str):
    requests.get(bib+"Default/search.aspx")
#    print(r1.status_code, r1.reason)
    data = {
        "query": {
            "Page":0,
            "PageRange":3,
            "QueryString":search_str,
            "ResultSize":100,
            "ScenarioCode":"DEFAULT",
            "SearchContext":0,
            "SearchLabel":"",
        }
    }
    r = requests.post(bib+"Default/Portal/Recherche/Search.svc/Search",json=data)
#    print(r3.status_code, r3.reason)
#    res = search['d']['Results'][0]['Resource']
#    print(search['d']['Results'][1]['Resource'])
    res = r.json()
    return [ get_book_infos(b) for b in res['d']['Results'] ]

def get_site_infos(s):
    res = { k : v for k,v in s.items() if k in ['Site','IsAvailable','HoldingId']}
    for e in s['Other']:
        if e['Key'] == 'InstitutionWording':
            res['Name'] = e['Value']
        elif e['Key'] == 'SiteLabelLink':
            res['Link'] = e['Value']
    return res

def get_holding(rsc_id):
    requests.get(bib+"Default/search.aspx")
#    print(r1.status_code, r1.reason)
    data = {  "Record":{ "RscId":rsc_id, "Docbase":"SYRACUSE", "PazPar2Id":"0_OFFSET_0"}  }
    r = requests.post(bib+"Default/Portal/Services/ILSClient.svc/GetHoldings",json=data)
#    print(r.status_code, r.reason)
    res = r.json()
    return [ get_site_infos(e) for e in res['d']['Holdings'] if e['IsAvailable'] ]

def get_holdings(rsc_id):
    return [ get_holding(e) for e in rsc_id ]
