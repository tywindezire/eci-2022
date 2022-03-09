import os
from flask import Flask
from flask import render_template,request
from flask import url_for


app = Flask('MyHerokuApp')
port = int(os.environ.get("PORT", 5000))
value=[]
nor=5
global mainlist
mainlist=[]
headers=['Leading party','	Leading party candidate','	Trailing party','	Trailing party candidate','	Margin']


@app.route("/")
def main():
    #return render_template("index.html",value=url_for('static',filename='/DATA/list_main.csv'))
    return render_template("index.html",value='/static/DATA/list_main.csv')


app.run(host='0.0.0.0', port=port, debug=True)
