class Date:
	"""docstring for booking"""
	def __init__(self, message,userid,token,customer_statuses,stores,customer_profiles,order_list,store_profiles):
		super(Date, self).__init__()
		self.message = message
		self.userid = userid
		self.token = token
		self.customer_statuses = customer_statuses
		self.stores = stores
		self.customer_profiles = customer_profiles
		self.order_list = order_list
		self.store_profiles=store_profiles

	def Date_choice(self):
		from linebot.models import (
		    MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,MessageTemplateAction,CarouselTemplate,CarouselColumn,ButtonsTemplate
		)
		from datetime import datetime  
		from datetime import timedelta  
		import requests

		date=requests.post('http://127.0.0.1:4000/check_date', json={"store":self.message}).json()['Remaining_date']
			
		action=[]
		for i in date :
			button=MessageTemplateAction(
        		label=i,
                text=i
             )
			action.append(button)


		date_choice=TemplateSendMessage(
		    alt_text='Buttons template',
		    template=ButtonsTemplate(
		        title='日期選擇',
		        text='請選擇則要訂餐的日期',
		        actions=action
		    )
		)

		error_message_1=TextSendMessage(text='您尚未開始定位流程')
		error_message_2=TextSendMessage(text='您尚未完成上一個訂位流程')

		if self.customer_statuses.find_one({"UID": self.userid})==None:
			return error_message_1
		else:
			if self.customer_statuses.find_one({"UID":self.userid})["status"]==2 :
				if self.stores.find_one({"store_name":self.message})==None:
					store={
						"store_name":self.message,
						"order_date":datetime.now().strftime("%Y-%m-%d"),
						"R_ID_list":[]
						}
					self.stores.insert_one(store).inserted_id
					detail={}
					store=self.store_profiles.find_one({"store_name":self.message})
					delte=['_id','total_seat','ntable','store_name']
					for i in delte:
						store.pop(i, None)
					for key in store:
						detail[key]=0
					self.stores.update_one({"store_name": self.message},{"$set":detail})
				self.customer_statuses.update_one({"UID": self.userid},{"$set":{"status":3}})
				return date_choice

			elif self.customer_statuses.find_one({"UID":self.userid})["status"]==1:
				return error_message_1
			else:
				return error_message_2

			
		

		# if self.customer_profiles.find_one({"UID": self.userid})==None:
		# 	customer_profile={
		# 		"UID":self.userid,
		# 		"name":"",
		# 		"phone":"",
		# 		"H_R_ID":[]
		# 		}
		# 	customer_status={
		# 		"UID":self.userid,
		# 		"status":2
		# 		}																		
		# 	self.customer_profiles.insert_one(customer_profile).inserted_id
		# 	self.customer_statuses.insert_one(customer_status).inserted_id
		# 	return restaurant_choice
		# else:
		# 	if self.customer_statuses.find_one({"UID": self.userid})==None:
		# 		customer_status={
		# 			"UID":self.userid,
		# 			"status":2
		# 			}
		# 		self.customer_statuses.insert_one(customer_status).inserted_id
		# 		return restaurant_choice
		# 	elif self.customer_statuses.find_one({"UID": self.userid})["status"]==1:
		# 		self.customer_statuses.update_one({"UID": self.userid},{"$set":{"status":2}})
		# 		return restaurant_choice
			
		# 	else:
		# 		return error_message



	

