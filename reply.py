class reply:


	def __init__(self, message,userid,token):
		super(reply, self).__init__()
		self.message = message
		self.userid = userid
		self.token = token
	def reply_message(self):
		from linebot import (
	    LineBotApi, WebhookHandler
		)
		from linebot.exceptions import (
		    InvalidSignatureError
		)
		from linebot.models import (
		    MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,MessageTemplateAction,CarouselTemplate,CarouselColumn,ButtonsTemplate
		)
		line_bot_api = LineBotApi('eIsju1O/B1taZCAdD2QmztlOEqwV22/0Pfjmzi0fTzykfkXfXXNtoFOqAMgcVntcKWlpHpbsM+8oTwk5nI40fvCsD8HKO2Rav5IRh+oHFh1T4tab5fBRGzMBJZOi3Ku2tJ4hLmbbXMmyzLbcsGZvZgdB04t89/1O/w1cDnyilFU=')
		handler = WebhookHandler('b2bf2bdb11b75c427266d4da18582649')
		line_bot_api.reply_message(
			self.token,
			TextSendMessage(text="test")
			)
				

