from flask import Flask,render_template,request
import pandas as pd
import requests


import model


api_key = "5c5c6788f7ca445284b2962146249e0a"
symbol = 'BTC/USD'
interval = '5min'
order = 'asc'

date = 0

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sub",methods=['POST'])
def submit():
    if request.method == "POST":
         train_start = request.form['a']
         train_end = request.form['b']
         test_start = request.form['c']
         test_end = request.form['d']
         global date
         date = test_end
         
         #  print( train_start, train_end,test_start, test_end)
        
         data = requests.get(f'https://api.twelvedata.com/time_series?symbol={symbol}&start_date={train_start}&end_date={train_end}&interval={interval}&order={order}&apikey={api_key}').json()
         train_data = pd.DataFrame(data['values'])
         train_data.to_csv('train.csv',index=False)

         data = requests.get(f'https://api.twelvedata.com/time_series?symbol={symbol}&start_date={test_start}&end_date={test_end}&interval={interval}&order={order}&apikey={api_key}').json()
         test_data = pd.DataFrame(data['values'])
         test_data.to_csv('test.csv',index=False)
         return render_template('ack.html')

@app.route("/res",methods=['POST'])
def results():
    if request.method == "POST":
        prediction = model.predict_price()
        # print(prediction)
        return render_template('result.html',pre = prediction, dt = date)


if __name__ == "__main__":
    app.run(debug=True)