from flask import Flask, request, redirect, url_for
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from stocker_database_setup import Base, Basic_information
import json

# Read file databaseAccount.json in directory critical_flie
# then can get database username and password.
with open('./critical_flie/databaseAccount.json') as accountReader:
    dbAccount = json.loads(accountReader.read())

app = Flask(__name__)

engine = create_engine(
    """mysql+pymysql://%s:%s@localhost/stocker?charset=utf8""" % (
            dbAccount["username"], dbAccount["password"]))
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def showMain():
    return "Main"


@app.route('/api/v0/Basic_information', methods=['POST'])
def handleBasicInfo():
    if request.method == 'POST':
        newBasicInfo = Restaurant(
            id=request.data['id'],
            type=request.data['type'],
            公司名稱=request.data['公司名稱'],
            公司簡稱=request.data['公司簡稱'],
            產業類別=request.data['產業類別'],
            外國企業註冊地國=request.data['外國企業註冊地國'],
            住址=request.data['住址'],
            營利事業統一編號=request.data['營利事業統一編號'],
            董事長=request.data['董事長'],
            總經理=request.data['總經理'],
            發言人=request.data['發言人'],
            發言人職稱=request.data['發言人職稱'],
            代理發言人=request.data['代理發言人'],
            總機電話=request.data['總機電話'],
            成立日期=request.data['成立日期'],
            上市上櫃興櫃公開發行日期=request.data['上市上櫃興櫃公開發行日期'],
            普通股每股面額=request.data['普通股每股面額'],
            實收資本額=request.data['實收資本額'],
            已發行普通股數或TDR原發行股數=request.data['已發行普通股數或TDR原發行股數'],
            私募普通股=request.data['私募普通股'],
            特別股=request.data['特別股'],
            編製財務報告類型=request.data['編製財務報告類型'],
            普通股盈餘分派或虧損撥補頻率=request.data['普通股盈餘分派或虧損撥補頻率'],
            普通股年度現金股息及紅利決議層級=request.data['普通股年度現金股息及紅利決議層級'],
            股票過戶機構=request.data['股票過戶機構'],
            過戶電話=request.data['過戶電話'],
            過戶地址=request.data['過戶地址'],
            簽證會計師事務所=request.data['簽證會計師事務所'],
            簽證會計師一=request.data['簽證會計師一'],
            簽證會計師二=request.data['簽證會計師二'],
            英文簡稱=request.data['英文簡稱'],
            英文通訊地址=request.data['英文通訊地址'],
            傳真機號碼=request.data['傳真機號碼'],
            電子郵件信箱=request.data['電子郵件信箱'],
            投資人關係聯絡人=request.data['投資人關係聯絡人'],
            投資人關係聯絡人職稱=request.data['投資人關係聯絡人職稱'],
            投資人關係聯絡電話=request.data['投資人關係聯絡電話'],
            投資人關係聯絡電子郵件=request.data['投資人關係聯絡電子郵件'],
            公司網站內利害關係人專區網址=request.data['公司網站內利害關係人專區網址'])
        session.add(newBasicInfo)
        session.commit()
        return redirect(url_for("showMain"))


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
