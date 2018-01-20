from __future__ import unicode_literals # 中文字比對用
from flask import Flask, request, abort
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
from datetime import datetime 
from datetime import timedelta 

# MongoDB config
client = MongoClient()
client = MongoClient('localhost', 27017)
client = MongoClient('mongodb://localhost:27017/')
db = client.booking
order_list = db.order_list
store_profiles =db.store_profiles


app = Flask(__name__)

api = Api(app)
class Remaining_seat_date(Resource): #finish
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('store', type=str)
        self.parser.add_argument('Remaining_date', type=str)
    def get(self):
        result = {'store': 'store\'sname <str>', 'Remaining_date':'still can booking date <str>'}
        return result
    def post(self):
        args=self.parser.parse_args()
        print ('API GOT:', args, type(args))
        # 因為button 只能顯示四個 因此查詢未來四天 
        # 如果未來要加 在討論
        week=[]
        [week.append((datetime.now()+timedelta(days=x)).strftime("%Y-%m-%d")) for x in range(0,4)]
        show=[]
        [show.append(week[x]) if order_list.find( { "store_name": args["store"] ,"order_date":week[x]} ).count()<store_profiles.find_one( { "store_name": args["store"] })["total_seat"] else week for x in range(0,4)] 
        args["Remaining_date"]=show

        return args
api.add_resource(Remaining_seat_date, '/check_date')
if __name__ == "__main__":
    app.run(port='4000')
