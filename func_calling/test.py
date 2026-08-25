import requests 

def get_order(user_id):
    url = f"http://localhost:8000/delivery/{user_id}"
    response = requests.get(url)
    result = response.json()
    return result 

output = get_order(4)
print(output)