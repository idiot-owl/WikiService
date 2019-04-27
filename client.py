import requests
import json

url="http://127.0.0.1:5000/"
headers={"content-type":"application/json"}


post_parameters = {"id": 1, "fields": ["type"]}
post_parameters = json.dumps(post_parameters)
result = requests.post(url=url, headers=headers, data=post_parameters) 
print("Status Code: " + str(result.status_code))
print("Result: " + str(json.loads((result.content))))

update_parameters = {"id": 1, "addFields": ["title"], "removeFields": ["title", "type"]}
update_parameters = json.dumps(update_parameters)
result = requests.put(url=url, headers=headers, data=update_parameters) 
print("Status Code: " + str(result.status_code))
print("Result: " + str(json.loads((result.content))))

get_parameters = {"id": 1, "fields": ["title"]}
get_parameters = json.dumps(get_parameters)
result = requests.get(url=url, headers=headers, data=get_parameters) 
print("Status Code: " + str(result.status_code))
print("Result: " + str(json.loads((result.content))))

delete_parameters = {"id": 2}
delete_parameters = json.dumps(delete_parameters)
result = requests.delete(url=url, headers=headers, data=delete_parameters) 
print("Status Code: " + str(result.status_code))
print("Result: " + str(json.loads((result.content))))


