# ccc={'a':1,'b':2}
# detail={}
# for key in ccc:
# 	print(key)
# 	detail[key]=0

# print(detail)

import requests


r=requests.post('http://127.0.0.1:5000/check_date', json={"store":"貳樓"}).json()['Remaining_date']
print(r)