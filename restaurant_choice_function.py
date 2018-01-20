class restaurant:
	def __init__(self,message,userid,TextSendMessage,TemplateSendMessage,MessageTemplateAction,CarouselTemplate,CarouselColumn,customer_statuses,stores,customer_profiles,order_list):
		super(restaurant, self).__init__()
		self.message = message
		self.userid = userid
		self.TextSendMessage= TextSendMessage
		self.TemplateSendMessage= TemplateSendMessage
		self.MessageTemplateAction= MessageTemplateAction
		self.CarouselTemplate= CarouselTemplate
		self.CarouselColumn= CarouselColumn
		self.customer_statuses = customer_statuses
		self.stores = stores
		self.customer_profiles = customer_profiles
		self.order_list = order_list
	def restaurant_choice(self):
		restaurant_choice=self.TemplateSendMessage(
						alt_text='Carousel template',
						template=self.CarouselTemplate(
							columns=[
								self.CarouselColumn(
									title='貳樓',
			                        text='貳樓餐廳阿',
			                        actions=[
			                        	self.MessageTemplateAction(
			                        		label='選擇',
			                                text='貳樓',
			                                )
			                            ]
			                       	),
			                    self.CarouselColumn(
			                        title='西堤',
			                        text='西堤餐廳喔',
			                        actions=[
			                            self.MessageTemplateAction(
			                            	label='選擇',
			                                text='西堤',
			                            	)
			                    		]
			                          )
			                    ]
		                	)
		           	 	)
		error_message=self.TextSendMessage(text='您尚未完成上一個訂位流程')

		if self.customer_profiles.find_one({"UID": self.userid})==None:
			customer_profile={
				"UID":self.userid,
				"name":"",
				"phone":"",
				"H_R_ID":[]
				}
			customer_status={
				"UID":self.userid,
				"status":2
				}																		
			self.customer_profiles.insert_one(customer_profile).inserted_id
			self.customer_statuses.insert_one(customer_status).inserted_id
			return restaurant_choice
		else:
			if self.customer_statuses.find_one({"UID": self.userid})==None:
				customer_status={
					"UID":self.userid,
					"status":2
					}
				self.customer_statuses.insert_one(customer_status).inserted_id
				return restaurant_choice
			elif self.customer_statuses.find_one({"UID": self.userid})["status"]==1:
				self.customer_statuses.update_one({"UID": self.userid},{"$set":{"status":2}})
				return restaurant_choice
			
			else:
				return error_message



	

