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
	ht = ht.replace(',',';')
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
		for items in te:
			items.strip()
		#print(te)
		newte = te[0:1]+te[2:4]+te[15:17]+te[28:30]
		if(newte[1] == 'i'):
			newte = newte[0:1]+['-','-','-','-','-','Counting Not Started']
		#print(newte)
		file_handle.write(str(newte).replace('[','').replace(']','').replace("'",'').replace(', ',',')+"\n")


def get_state_data(state_name,state_code,max_constituency):
	f = open("./static/DATA/"+state_name+".csv",'w')
	for i in range(1,max_constituency+1):
		#print(str(i)+"/"+str(max_constituency),end=" ")
		parseResults('https://results.eci.gov.in/ResultAcGenMar2022/statewiseS'+str(state_code)+str(i)+'.htm',f)
	print(state_name)

def parseParty(url,file_handle):
	major_party_list = ['Bahujan Samaj Party','Bharatiya Janata Party','Indian National Congress','Aam Aadmi Party']
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
		if(te[0] in major_party_list):
			newte = te[0:4]
			file_handle.write(str(newte).replace('[','').replace(']','')+"\n")
			
def main_result():
	states = ['UttarPradesh','Punjab','Goa','Manipur','Uttarakhand']
    	website_code = ['24','19','05','14','28']
    	max_constituency = [41,12,4,6,7]
	#for i in range(5):
	#	parseParty('https://results.eci.gov.in/ResultAcGenMar2022/partywiseresult-S'+website_code[i]+'.htm',open('./static/DATA/'+states[i]+'_party_data.csv','w'))
	#	get_state_data(states[i],website_code[i],max_constituency[i])
	get_state_data('UttarPradesh','24',41)
	get_state_data('Punjab','19',12)
	get_state_data('Goa','05',4)
	get_state_data('Manipur','14',6)
	get_state_data('Uttarakhand','28',7)
	parseParty('https://results.eci.gov.in/ResultAcGenMar2022/partywiseresult-S24.htm',open('./static/DATA/UttarPradesh_party_data.csv','w'))
	parseParty('https://results.eci.gov.in/ResultAcGenMar2022/partywiseresult-S19.htm',open('./static/DATA/Punjab_party_data.csv','w'))
	parseParty('https://results.eci.gov.in/ResultAcGenMar2022/partywiseresult-S05.htm',open('./static/DATA/Goa_party_data.csv','w'))
	parseParty('https://results.eci.gov.in/ResultAcGenMar2022/partywiseresult-S14.htm',open('./static/DATA/Manipur_party_data.csv','w'))
	parseParty('https://results.eci.gov.in/ResultAcGenMar2022/partywiseresult-S28.htm',open('./static/DATA/Uttarakhand_party_data.csv','w'))
#get_state_data('UttarPradesh','24',41)
#get_state_data('Punjab','19',12)
#get_state_data('Goa','05',4)
#get_state_data('Manipur','14',6)
#get_state_data('Uttarakhand','28',7)
#================================================================================================================

@app.route("/")
def main():

    #return render_template("index.html",value=url_for('static',filename='/DATA/list_main.csv'))
    #for i in range(5):
	#parseParty('https://results.eci.gov.in/ResultAcGenMar2022/partywiseresult-S'+website_code[i]+'.htm',open('./static/DATA/'+states[i]+'_party_data.csv','w'))
	#get_state_data(states[i],website_code[i],max_constituency[i])
    main_result()
    return render_template("index.html",value='/static/DATA/list_main.csv')



app.run(host='0.0.0.0', port=port, debug=True)
