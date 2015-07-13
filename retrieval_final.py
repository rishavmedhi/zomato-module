#retreival code for the zomato module 

'''list of queries handled
	#(restaurant name) restaurant in (city-name)
	#phone no/contact no of (restaurant name) restaurant (location+searching)
	#restaurants near me
	#food places near me
	#places to eat near me
	#where is food-place restaurant in place-name'''

#using mongo database zomato and collection res

import pymongo
client = pymongo.MongoClient()
#using mongo database zomato and collection res
mdb = client['zomato']
qb=mdb['res']

#fuction for extracting location from server
def locfrmuser(lati,longi):
	lati=float(lati)
	longi=float(longi)
	return [lati,longi]

points=[12.8233113,80.0421151]

#taking input from user
#query=raw_input("Enter? ").lower()
#orig_query=query

#removal of stop words
def resmain(query):
	orig_query=query
	#points=locfrmuser()
	ans={}
	anslist=[]
	if "restaurant" in query or "restaurants" in query or "place" in query or 'food' in query or 'eat' in query:
		wrd=['restaurants','restaurant','location','address','phone','contact','no.',' no ','contact','near','places','place','me','food','eat',' to ',' is ','where','of ']
		for i in wrd:
			query=query.replace(i,"")
		print query

		if " in " in query:
			query=query.replace(" in "," ")
			print query
			query=query.rsplit(" ",1)
		else:
			query=query.rsplit(" ",1)
			print query
		print query
		flag=0 
		
		#checking if query is goes empty after discarding process
		if len(query)!=1:
			resname=query[0].strip()
			place=query[1].strip()
			query1=''
			print len(resname)
			if len(resname)!=0:
				query1="\s?"+str(resname)+"\s?"
			#query2="\s?"+str(place)+"\s?"
				
				#restaurant name and address can be extracted
				if len(place)!=0 and len(query1)!=0:
				
					#check if phone or contact no is asked by user
					if ("contact" in orig_query or "phone" in orig_query) and flag==0:
						for i in qb.find({"title":{"$regex":str(query1),"$options":"i"},"address":{"$regex":str(place),"$options":"i"}}).limit(1):
							anslist.append(i)
						flag=1

					#searching by restaurant name and place
					results=qb.find({"title":{"$regex":str(query1),"$options":"i"},"address":{"$regex":str(place),"$options":"i"}}).count()
					if(results !=0) and flag==0:
						for i in qb.find({"title":{"$regex":str(query1),"$options":"i"},"address":{"$regex":str(place),"$options":"i"}}):
							anslist.append(i)
						
						flag=1
					
				#searching only if restaurant name is found
				if ("contact" in orig_query or "phone" in orig_query) and flag==0:
						for i in qb.find({"title":{"$regex":str(query1),"$options":"i"},"loc":{"$near":{"$geometry":{"type":"Point","coordinates":points}}}}).limit(1):
							anslist.append(i)
						flag=1
				
				#searching for nearest restaurant with the name present
				if query1!='' and flag==0:
						for i in qb.find({"title":{"$regex":str(query1),"$options":"i"},"loc":{"$near":{"$geometry":{"type":"Point","coordinates":points}}}}).limit(10):
							anslist.append(i)
						flag=1

			#searching for all restaurants near the user's location
			if flag==0:
				for i in qb.find({"loc":{"$near":{"$geometry":{"type":"Point","coordinates":points}}}}).limit(20):
					anslist.append(i)
				flag=1
			
			#return empty if result is not found
			if flag==0:
				return [{}]
				
			#return result
			if flag==1:
				ans={"restaurant":anslist}
				return [ans]		
