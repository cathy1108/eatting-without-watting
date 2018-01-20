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

		restaurant_choice=TemplateSendMessage(
						alt_text='Carousel template',
						template=CarouselTemplate(
							columns=[
								CarouselColumn(
									title='貳樓',
			                        text='貳樓餐廳阿',
			                        actions=[
			                        	MessageTemplateAction(
			                        		label='選擇',
			                                text='貳樓',
			                                )
			                            ]
			                       	),
			                    CarouselColumn(
			                        title='西堤',
			                        text='西堤餐廳喔',
			                        actions=[
			                            MessageTemplateAction(
			                            	label='選擇',
			                                text='西堤',
			                            	)
			                    		]
			                          )
			                    ]
		                	)
		           	 	)
		error_message=TextSendMessage(text='您尚未完成上一個訂位流程')

		if self.stores.find_one({"store_name":self.message})==None:

			store={
				"store_name":self.message,
				"order_date":datetime.now().strftime("%Y-%m-%d"),
				"R_ID_list":[],
			}
			self.stores.insert_one(store).inserted_id
			detail={}
			store=self.store_profiles.find_one({"store_name":self.message})
			for i in range(3,len(list(store.keys()))):
				detail[list(store.keys())[i]]=0
			self.stores.update_one({"store_name": self.message},{"$set":detail})
		

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



	

