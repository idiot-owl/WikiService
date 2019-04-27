import json
import requests

# Checking if the current data is a uel containing json
def check_if_json(curr_data, curr_field):
    try:
        temp_data = curr_data[curr_field]
        temp_data = json.loads((requests.get(temp_data)).content)
    except:
        return False
    return temp_data
    
# Checking if the current data is in a list format  
def check_if_list(curr_data, curr_field):
    try:
        temp_field_index = curr_field.find('[')
        temp_field = curr_field[:temp_field_index]
        temp_data = curr_data[temp_field]
        temp_field = 'temp_data' + curr_field[temp_field_index:]
        temp_data = eval(temp_field)
    except:
        return False
    return temp_data
