from pymongo import MongoClient
from datetime import datetime 
from datetime import timedelta 
import requests

# MongoDB config
client = MongoClient()
client = MongoClient('localhost', 27017)
client = MongoClient('mongodb://localhost:27017/')
db = client.booking

customer_statuses = db.customer_statuses
customer_profiles = db.customer_profiles
order_list = db.order_list
stores = db.stores
store_profiles =db.store_profiles

a=datetime.now()
b=datetime(a.year,a.month,a.day,0,0,0)
number=int((round((a-b).total_seconds(),2))*100)

order={
	"UID":number+1,
	"R_ID":number,
	"store_name":"貳樓",
	"order_date":(datetime.now()+timedelta(days=1)).strftime("%Y-%m-%d"),
	"n_pepole":5,
	"slot":"1200-1230",
	"enter_time":"",
	"end_tiime":""
	}
order_list.insert_one(order).inserted_id

# store_profile={
# 	"store_name":"貳樓",
# 	"ntable":[2,4],
# 	"2_table":{"total":3,"1200-1230":1,"1230-1300":1,"1300-1330":1},
# 	"4_table":{"total":4,"1200-1230":2,"1230-1300":1,"1300-1330":1},
# 	"total_seat":7
# }
# store_profiles.insert_one(store_profile).inserted_id

# a=order_list.find( { "store_name": "貳樓" } )
# count=0
# for i in range(0,a.count()):
# 	print(a[i])
# 	if a[i]["order_date"]=="2018-01-10":
# 		count+=1
# print(count)

# week=[]
# [week.append((datetime.now()+timedelta(days=x)).strftime("%Y-%m-%d")) for x in range(0,8)]
# show=[]
# [show.append(week[x]) if order_list.find( { "store_name": "貳樓" ,"order_date":week[x]} ).count()<store_profiles.find_one( { "store_name": "貳樓" })["total_seat"] else week for x in range(0,8)] 
# print(show)
# print(week)

# x=1
# print(order_list.find( { "store_name": "貳樓" ,"order_date":week[x]} ).count())


# print(week)







# for i in range(0,8):
# 	week.append((datetime.now()+timedelta(days=i)).strftime("%Y-%m-%d"))


# r=requests.post('http://127.0.0.1:3000/check_date', json={"store":"貳樓"})
# print(r.json()['Remaining_date'])