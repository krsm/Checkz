import requests

payload = {'user_id':76}
r = requests.get('http://127.0.0.1:500/get_favorite_places/', payload)

print(r.url)