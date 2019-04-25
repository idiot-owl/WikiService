import requests
import json

result = requests.get('https://en.wikipedia.org/api/rest_v1/page/summary/Stack_Overflow')
print(result.content)