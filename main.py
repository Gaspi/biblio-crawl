# -*- coding: utf-8 -*-

import requests, re
from bs4 import BeautifulSoup

bib = "https://bibliotheques.paris.fr/"

def get_book_infos(imagelinks,b):
    bookid=b['Resource']['RscId']
    return {'RscId' : bookid,
            'Title' : b['Resource']['Ttl'],
            'Link'  : b['FriendlyUrl'],
            'Img' : imagelinks.get( bookid ),
            }

def get_imagelink(rscid):
    link = bib + "Default/doc/SYRACUSE/" + str(rscid)
    r = requests.get(link)
    soup = BeautifulSoup(r.text, features="html5lib")
    title = soup.find("div", {'id':'notice_longue_description'}).find('h2').text
    bookimg = re.findall("://(.*)/MEDIUM?",soup.find("img")['src'])
    img = bookimg[0] if len(bookimg)>0 else None
    return {'RscId' : rscid,
            'Title' : title,
            'Link'  : link,
            'Img'   : img }

def get_imagelinks(rscids):
    return [ get_imagelink(rscid) for rscid in rscids ]


def search_book(search_str):
    requests.get(bib+"Default/search.aspx")
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
    res = r.json()

    imagelinks={}
    soup = BeautifulSoup(res['d']['HtmlResult'], features="html5lib")
    for c in soup.findAll("div",{ "class":"notice_container"}):
        v = c.find("div",{"class":"vignette_document"}).find("a")
        bookid  = re.findall("SYRACUSE/(.*)/",v['href'])
        bookimg = re.findall("://(.*)/MEDIUM?",v.find("img")['src'])
        if bookid and len(bookid)>0 and len(bookimg)>0:
            imagelinks[bookid[0]] = bookimg[0]
    return [ get_book_infos(imagelinks,b) for b in res['d']['Results'] ]

def get_site_infos(s):
    res = { 'Site'        : s['Site'],
            'IsAvailable' : s['IsAvailable'],
            'SiteCode'    : s['SiteCode'] };
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

scores = { '75014' : 10, '75013' : 9, '75005' : 8, '75015' : 7, '75006' : 6, '75007' : 5, '75004' : 4, '75001' : 3 }
def score_dist(s):
    arr = s.split(" - ")[0]
    return scores[arr] if arr in scores else 0

def get_holdings(rsc_id):
    sites = { }
    holdings = { }
    for e in rsc_id:
        hs = get_holding(e)
        holdings[e] = [ h['SiteCode'] for h in hs]
        for h in hs:
            if h['SiteCode'] not in sites:
                sites[ h['SiteCode'] ] = {
                        'Site' : h['Site'],
                        'Name' : h['Name'],
                        'Link' : h['Link'],
                        'Count': 1  }
            else:
                sites[ h['SiteCode'] ]['Count'] +=1
    def key(i):
        return (i[1]['Count'] , score_dist(i[1]['Site']) )
    sites = [ dict({'SiteCode':k},**v) for k,v in sorted(sites.items(), reverse=True, key=key)]
    return (sites, holdings)
