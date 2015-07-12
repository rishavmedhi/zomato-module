import threading
import urllib2
from bs4 import BeautifulSoup
import pymongo
client = pymongo.MongoClient()
mdb = client['zomato']
qb=mdb['restaurants2']
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

def call(link):
	try:
		print "inside function"
		details=link
		result={}
		page=urllib2.urlopen(details["link"]).read()
		soup=BeautifulSoup(page)
		data=soup
		tel=data.find("span","tel")
		phno=tel.get_text(",").encode("utf-8").strip()
		x=data.find("div","res-main-address-text")
		if not x:
			address="none"
		else:
			address=x.get_text(" ").encode("utf-8").strip()
		ctr=0
		cusines=" "
		estb=" "
		for link in data.find_all("div","res-info-cuisines clearfix"):
			ctr=ctr+1
			if(ctr==1): 
				cuisines=link.get_text().encode("utf-8").strip()
				continue
			#if(ctr==2): 
				#estb=link.get_text().encode("utf-8").strip()
				#continue
		#cuisine=x.get_text().strip()
		x=data.find("div","res-week-timetable")
		timings=x.find("span","left")
		times=timings.get_text().encode("utf-8") 
		x=data.find("span",itemprop="priceRange")
		if not x:
			pricer="not available"
		else:
			pricer=x.get_text().encode("utf-8").strip()
		lclink=data.find("div","resmap-img")
		if not lclink:
			loc="not available"
		else:
			style=lclink.get('style')
			loc=style.split("|")
			loc=str(loc[2]).encode("utf-8")
			loc1="["+loc+"]"
			loc=eval(loc1)
		#phno,address,cuisines,estb,times,pricer
		title=details["name"]
		if "'" in title or "-" in title:
			title=title.replace("'","")
			title=title.replace("-","")
		
		result={"name":details["name"],"city":details["city"],"tel_no":phno,"address":address,"cuisines":cuisines,"timings":times,"price":pricer,"location":loc,"title":title}
		qb.insert(result)
		print result
	except Exception as e:
		print "here"
		print e
		wdata=str(details["name"]+" "+details["city"]+",")
		
		#logging exceptions in file
		foe=open("excep.txt","a")
		foe.write(wdata)
		foe.close()
		
		pass
	
def respage(res):
	T=threading.Thread
	#url="https://www.zomato.com/chennai/absolute-barbecue-t-nagar"
	i=0
	print "starting thread"
	print len(res)
	#result={}
	#url=link["link"]
	while threading.activeCount()<150:
		t=T(target=call,args=(res[i],))
		t.start()
		i=i+1
