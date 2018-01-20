# -*- coding: utf-8 -*-
# from flask_restful import Resource, Api

class bot_speaker:
    def __init__(self, line_bot_api, TextSendMessage):
        self.line_bot_api = line_bot_api
        self.TextSendMessage = TextSendMessage


    '''module 導入測試'''
    def hello_world(self):
        print ({'still': 'alive'})
        return {'still': 'alive'}


    '''給 LineBot & Website 使用的叫號功能'''
    def Broadcast_ONE(self, UID, messaged):
        print ("Broadcast_ONE Function")
        self.line_bot_api.push_message(UID, self.TextSendMessage(text=message))
        return 'Success'




# message_list = {'維霖': 'U4a561060f2c3273a3323cde8650f42c1',
#                 '李奕': 'XXXXX',
#                 '凱西': 'XXXXX'}