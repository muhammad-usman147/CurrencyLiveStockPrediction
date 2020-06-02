from flask import Flask,request,redirect
from usdcad import predict 
from flask import render_template
from eurusd import Eurusdpredict
from gbpusd import PredictGbpusd
from usdjpy import predictUsdJpy
from xauusd import predictXauUsd
from datetime import datetime
import pandas as pd 
import numpy as np
import requests
app = Flask(__name__)
print(app)

@app.route('/') #home
def Auth():
    return render_template('form.html')
@app.route('/login')
def Login():
    return render_template('login.html')
@app.route('/login/check',methods = ['POST'])
def checkuser():
    if request.form.get('uname') == 'admin' and request.form.get('psw') == 'admin1234':
        return redirect('/getdata')
    else:
        return redirect('/')
@app.route('/getdata')
def GetData():
    opens = []
    close = []
    high = []
    low = []
    currency = []
    data_to_get = ['GBPUSD','EURUSD','USDJPY','XAUUSD','USDCAD']
    get = {}
    d = requests.get(f'https://marketdata.tradermade.com/api/v1/historical?api_key=sV28dANyN4J6CsS_eCho&date=2020-05-31&currency=USDCAD').json()['date']
    for i in data_to_get:
        data = requests.get(f'https://marketdata.tradermade.com/api/v1/historical?api_key=sV28dANyN4J6CsS_eCho&date=2020-05-31&currency={i}').json()
        get[i] = data['quotes'][0] 
    prerictions = {}
    for cur in data_to_get:
        opens.append(get[cur]['open'])
        close.append(get[cur]['close'])
        high.append(get[cur]['high'])
        low.append(get[cur]['low'])
        currency.append(cur)
    inputs = {}
    inputs['cur'] = currency
    inputs['open'] = opens
    inputs['close'] = close
    inputs['high'] = high
    inputs['low'] = low

    
    prerictions['xdate'] = str(d)
    x = PredictGbpusd(opens[0],low[0],high[0],close[0])
    prerictions[currency[0]] = [x[0][0],x[0][1]]

    x = Eurusdpredict(opens[1],low[1],high[1],close[1])
    prerictions[currency[1]] = [x[0][0],x[0][1]]

    x = predictUsdJpy(opens[2],low[2],high[2],close[2])
    prerictions[currency[2]] = [x[0][0],x[0][1]]

    x = predictXauUsd(opens[3],low[3],high[3],close[3])
    prerictions[currency[3]] = [x[0][0],x[0][1]]

    x = predict(opens[4],low[4],high[4],close[4])
    prerictions[currency[4]] = [x[0][0],x[0][1]]

    pd.DataFrame(prerictions).to_csv('predictions.csv',index = False)
    data = pd.read_csv('predictions.csv')
    return render_template('table.html',data = data)
if __name__ == '__main__':
    app.run()













'''
def solvemefirst(a,b):
    return a + b
res = solvemefirst(2,3)
print(res)
'''
