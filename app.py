# -*- coding: utf-8 -*-
from __future__ import unicode_literals # 中文字比對用
from flask import Flask, request, abort
from flask_restful import Resource, Api, reqparse


from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,MessageTemplateAction,CarouselTemplate,CarouselColumn,ButtonsTemplate
)
# import pymongo
from pymongo import MongoClient

# MongoDB config
client = MongoClient()
client = MongoClient('localhost', 27017)
client = MongoClient('mongodb://localhost:27017/')
db = client.booking


# import datetime
from datetime import datetime  
from datetime import timedelta  

# custom
import API_function
import restaurant_choice_function
import date_choice_function




app = Flask(__name__)

# Cathy's key
line_bot_api = LineBotApi('eIsju1O/B1taZCAdD2QmztlOEqwV22/0Pfjmzi0fTzykfkXfXXNtoFOqAMgcVntcKWlpHpbsM+8oTwk5nI40fvCsD8HKO2Rav5IRh+oHFh1T4tab5fBRGzMBJZOi3Ku2tJ4hLmbbXMmyzLbcsGZvZgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('b2bf2bdb11b75c427266d4da18582649')
# Arctic's key
# line_bot_api = LineBotApi('FjojFyva1oiinVDu74X5RN2UUYFMt9ns4jMKsFMa+4ldgBnID/sAgNQiV9VXh62zhGRvdALMsPVYUfiBus1spthaaZdMDB6EWuoJQ1QjAUrRgHjqE6I0vA/JdKo83w10UhXcszSlZtIhKKbW+Ryw1gdB04t89/1O/w1cDnyilFU=')
# handler = WebhookHandler('bf4df327e2993e986866a3189f3fb472')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


# 沒有handler的event都會在這邊
@handler.default()
def default(event):
    print (event)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    userid=event.source.user_id

    #database
    customer_statuses = db.customer_statuses
    customer_profiles = db.customer_profiles
    order_list = db.order_list
    stores = db.stores
    store_profiles =db.store_profiles

    restaurant_list=["貳樓","西堤"]
    time=[]
    column=[]
    print ('type:', event.type)
    print ('UID:', userid, '\n說:', message)
    splited = message.split()

    #選擇餐廳 ==> 尚須改進
    '''
    1. rich menu 減少打字機會
    2. 餐廳button 自動化
    3. 解決多個餐廳button無法顯示問題

    '''
    if message=="訂位":
        restaurant= restaurant_choice_function.restaurant(
            event.message.text,event.source.user_id,
            TextSendMessage,TemplateSendMessage,MessageTemplateAction,CarouselTemplate,CarouselColumn,
            customer_statuses,stores,customer_profiles,order_list)
        reply=restaurant.restaurant_choice()
        line_bot_api.reply_message(
                event.reply_token,
                reply
            )

    #選擇訂位日期 ==> 尚須改進
    '''
    1. date picker 判斷 line 版本跳出??
    2. 商家端資料創建責任歸屬 web or bot

    '''

    if message in restaurant_list and customer_statuses.find_one({"UID":userid})["status"]==2 :
        date_choice= date_choice_function.Date(event.message.text,event.source.user_id,event.reply_token,customer_statuses,stores,customer_profiles,order_list,store_profiles)
        date_choice.Date_choice()
        # if stores.find_one({"store":message})==None:
        #     store = {"store": message,
        #             "date": datetime.now().strftime("%Y-%m-%d"),
        #             "booking_number":0,
        #             "watting_person":0,
        #             "早": 4,
        #             "中": 4,
        #             "晚": 4,
        #             "10:00~10:30": 1,
        #             "10:30~11:00": 1,
        #             "11:00~11:30": 1,
        #             "11:30~12:00": 1,
        #             "12:00~12:30": 1,
        #             "12:30~13:00": 1,
        #             "13:00~13:30": 1,
        #             "13:30~14:00": 1,
        #             "18:00~18:30": 1,
        #             "18:30~19:00": 1,
        #             "19:00~20:30": 1,
        #             "20:30~21:00": 1}
        #     stores.insert_one(store).inserted_id

        # if stores.find_one({"store": message})["早"]==0 and stores.find_one({"store": message})["午"]==0 and stores.find_one({"store": message})["晚"]==0 :
        #     line_bot_api.reply_message(
        #         event.reply_token,
        #         TextSendMessage(text="抱歉餐廳已客滿")
        #     )
        # else:
        #     posts.update_one({"author": userid},{"$set":{"restaurant":message,"status":2}})
        #     action=[]
        #     time=stores.find_one({"store":message})
        #     column= list(time.keys())
        #     for columns in range(8,12):
        #         button=MessageTemplateAction(
        #             label=column[columns],
        #             text=message+" "+column[columns]
        #         )
        #         action.append(button)
        #     line_bot_api.reply_message(
        #         event.reply_token,
        #             TemplateSendMessage(
        #                 alt_text='Buttons template',
        #                 template=ButtonsTemplate(
        #                     title='時段選擇',
        #                     text='請選擇要訂位的時段',
        #                     actions=action[:]
        #                 )
        #             )

        #     )

    if len(splited)==2:
        if splited[0]==posts.find_one({"author":userid})["restaurant"] and splited[1]!=None and posts.find_one({"author": userid})["status"]==2:
            a=datetime.datetime.now()
            b=datetime.datetime(a.year,a.month,a.day,0,0,0)
            number=int((round((a-b).total_seconds(),2))*100)
            posts.update_one({"author": userid},{"$set":{"Time_period":splited[1],"booking_number":number,"status":3}})
            stores.update_one({"store":posts.find_one({"author":userid})["restaurant"]},{"$inc":{"watting_person":1}})
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='您的訂位號碼為: '+str(number))
            )
    if message == "查詢" and posts.find_one({"author": userid})["status"]==3:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='目前叫號: '+str(stores.find_one({"store": posts.find_one({"author":userid})["restaurant"]})["booking_number"]))
        )


# todo: 重新導向 https://line.me/R/ti/p/uTLCY3Xoar
# 作法一  不使用Line login，需另外產生RID短碼(亂數4碼)
# 1. (商家端產生)Server網址帶RID參數，掃描先到某flask頁面
# 2. Server紀錄RID，跳轉到BOT對話窗
# 3-1. (未加好友)使用者加入，輸入RID短碼(亂數4碼)，BOT將UID與RID連結
# 3-2. (已加好友)使用者輸入RID短碼(亂數4碼)，BOT將UID與RID連結
# 4. 完成連結過程
# 作法二  使用Line login (待確認)
# 1. (商家端產生)Server網址帶RID參數，掃描到Line登入畫面
# 2. 使用者登入，加入BOT好友，系統紀錄UID與RID (待確認:只登入不加好友的情況)
# 3. 跳轉到BOT對話窗，BOT自動詢問 單號XXX是否為使用者單號?{YES/NO}
# 4. 完成連結過程


api = Api(app)
bot = API_function.bot_speaker(line_bot_api, TextSendMessage)
# str, unicode = unicode, str


class HelloWorld(Resource):
    
    def get(self):
        result = bot.hello_world()
        return result


class Broadcast_ONE(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('UID', type=str)
        self.parser.add_argument('message', type=str, required=True, help='Missing <message> arg.')

    def get(self):
        result = {'UID': 'user id <str>', 'message': 'say_message <str>'}
        return result

    def post(self):
        args = self.parser.parse_args()#strict=True)
        print ('API GOT:', args, type(args))
        result = bot.Broadcast_ONE(args['UID'], args['message'])
        args['result'] = result
        return args
class Remaining_seat_date(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('store_name', type=str)
        self.parser.add_argument('date', type=lambda x: datetime.strptime(x,'%Y-%m-%d'))
        self.parser.add_argument('Remaining_seat', type=str)
    def get(self):
        result = {'store': 'store\'sname <str>', 'date': 'order date <datetime>','Remaining_seat':'store have a seat at that date or not <str>'}
        return result
    def post(self):
        args=self.parser.parse_args()
        print ('API GOT:', args, type(args))
        

api.add_resource(HelloWorld, '/')
api.add_resource(Broadcast_ONE, '/say')

if __name__ == "__main__":
    app.run()