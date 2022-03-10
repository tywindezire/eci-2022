import os
from flask import Flask
from flask import render_template,request
from flask import url_for
import urllib.request, urllib.error, urllib.parse
import re


app = Flask('MyHerokuApp')
port = int(os.environ.get("PORT", 5000))
value=[]
nor=5
global mainlist
mainlist=[]
headers=['Leading party','	Leading party candidate','	Trailing party','	Trailing party candidate','	Margin']

#================================================================================================================
def remove_all_old(key,my_list):
	copy_list = my_list
	for items in my_list:
		if(items == key):
			copy_list.remove(items)
	while True:
			try:
				copy_list.remove('')
			except:
				break
	return copy_list

def remove_all(key,my_list):
	while True:
		try:
			my_list.remove(key)
		except:
			break


def parseResults(url,file_handle):
	response = urllib.request.urlopen(url)
	ht = response.read().decode('UTF-8')
	#print(ht)
	ht = ht.replace('\n','')
	ht = ht.replace('\r','')
	ht = ht.replace('  ','')
	mylist = ht.split("<tr style='font-size:12px;'>")[1:]
	for items in mylist:
		#print("==================================================================================================================================================================")
		mystr = items
		te = re.findall(r'(.*?)\<.*?\>', mystr)
		remove_all('',te)
		remove_all(' ',te)
		try:
			for items in te:
				if(items == ' '):
					print('Disaster')
					break
		except:
			pass
		#print(te)
		newte = te[0:1]+te[2:4]+te[15:17]+te[28:30]
		if(newte[1] == 'i'):
			newte = newte[0:1]+['-','-','-','-','-','Counting Not Started']
		#print(newte)
		file_handle.write(str(newte).replace('[','').replace(']','')+"\n")


def get_state_data(state_name,state_code,max_constituency):
	f = open("./static/DATA/"+state_name+".csv",'w')
	for i in range(1,max_constituency+1):
		#print(str(i)+"/"+str(max_constituency),end=" ")
		parseResults('https://results.eci.gov.in/ResultAcGenMar2022/statewiseS'+str(state_code)+str(i)+'.htm',f)
	print(state_name)

get_state_data('UttarPradesh','24',41)
get_state_data('Punjab','19',12)
get_state_data('Goa','05',4)
get_state_data('Manipur','14',6)
get_state_data('Uttarakhand','28',7)
#================================================================================================================

@app.route("/")
def main():
    #return render_template("index.html",value=url_for('static',filename='/DATA/list_main.csv'))
    return render_template("index.html",value='/static/DATA/list_main.csv')


app.run(host='0.0.0.0', port=port, debug=True)
