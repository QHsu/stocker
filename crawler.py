# coding=utf-8
import requests
import pandas as pd
import json
from datetime import datetime
from io import StringIO


def crawlCriticalInformation(parse_to_json=False):
    res = requests.get('https://mops.twse.com.tw/mops/web/ajax_t05sr01_1')
    res.encode = 'utf-8'
    dfs = pd.read_html(StringIO(res.text), header=0, flavor='bs4')
    ret = pd.DataFrame()

    if len(dfs) == 1:
        return ret
    # code, name, date, content

    # print(dfs[1])

    file = open('criticalInfo.json', 'r', encoding='utf-8')
    settings = json.loads(file.read())
    file.close()

    criteria_pos = settings["criteria_pos"]
    criteria_neg = settings["criteria_neg"]

    for index in range(0, len(dfs[1])):
        match = False
        for crp in criteria_pos:
            match = match or (dfs[1].iloc[index]['主旨'].find(crp) != -1)
            for crn in criteria_neg:
                if dfs[1].iloc[index]['主旨'].find(crn) != -1:
                    match = False

            if(match):
                    try:
                        tmp = dfs[1].iloc[index]
                        ret = ret.append(tmp)
                    except Exception as err:
                        print(err)
                    break
    if parse_to_json:
        colHeader = list(ret.columns.values)
        colHeader.pop(0)
        rowHeader = list(ret.index)
        # print(dfs.loc[rowHeader[1]])

        dataArr = []

        for i in rowHeader:
            try:
                tmpDict = {}
                for k in colHeader:
                    if k == '公司代號':
                        tmpDict[k] = str(int(ret.loc[i][k]))
                    else:
                        tmpDict[k] = ret.loc[i][k]
                dataArr.append(tmpDict)
            except Exception as err:
                print(err)

        ret = json.dumps(dataArr)
    return ret


def crawlBasicInformation(companyType):
    url = "https://mops.twse.com.tw/mops/web/ajax_t51sb01"
    headers = {
        'User-Agent': """Mozilla/5.0
                      (Macintosh; Intel Mac OS X 10_10_1)
                      AppleWebKit/537.36 (KHTML, like Gecko)
                      Chrome/39.0.2171.95 Safari/537.36""",
        'Content-Type': 'application/x-www-form-urlencoded',
        'encodeURIComponent': '1',
        'step': '1',
        'firstin': '1',
        'off': '1',
        'TYPEK': companyType,
    }
    result = requests.get(url, headers)
    print("crawler complete.")
    result.encoding = 'utf-8'
    html_df = pd.read_html(StringIO(result.text), header=0)
    print("parsing html to df")
    ret = html_df[0]
    
    # take out all special char out
    ret = ret.replace(r'\,', '/', regex=True)
    ret = ret.fillna("0")
    ret.columns = ret.columns.astype(str).str.replace('(','')
    ret.columns = ret.columns.astype(str).str.replace(')','')
    
    # remove invalid row
    drop_index = []
    for i in ret.index:
        if ret.iloc[i]["公司代號"] == "公司代號":
            drop_index.append(i)
    ret = ret.drop(ret.index[drop_index])
    
    return ret

def crawlMonthlyRevenue(westernYearIn, monthIn):
    year = str(westernYearIn - 1911)
    month = str(monthIn)

    urlOtcDomestic = "https://mops.twse.com.tw/nas/t21/sii/t21sc03_"\
                     + year  + "_"  + month  + "_0.html"
    urlOtcForiegn = "https://mops.twse.com.tw/nas/t21/sii/t21sc03_"\
                     + year + "_"+ month + "_1.html"
    urlSiiDomestic = "https://mops.twse.com.tw/nas/t21/otc/t21sc03_"\
                     + year  + "_"  + month  + "_0.html"
    urlSiiForiegn = "https://mops.twse.com.tw/nas/t21/otc/t21sc03_"\
                     + year + "_"+ month + "_1.html"

    urls = [urlOtcDomestic, urlOtcForiegn, urlSiiDomestic, urlSiiForiegn]

    results = pd.DataFrame()
    for url in urls:
        print("crawling...: "+url)
        req = requests.get(url)
        req.encoding = "big5"
        print("parsing html to df")
        html_df = pd.read_html(StringIO(req.text))
        dfs = pd.DataFrame()
        for df in html_df:
            if df.shape[1] == 11:
                dfs = pd.concat([dfs,df], axis=0, ignore_index=True)
        dfs.columns = dfs.columns.droplevel()

        drop_index = []
        for i in dfs.index:
            try:
                int(dfs.iloc[i]["公司代號"])
            except:
                drop_index.append(i)
        dfs = dfs.drop(dfs.index[drop_index])

        results = results.append(dfs)
    return results

if __name__ == "__main__":
    siiCompany = crawlBasicInformation('sii')
    #otcCompany = crawlBasicInformation('otc')
    print(type(siiCompany))
    #print(otcCompany)
