import requests 
from dotenv import load_dotenv
from openai import OpenAI 
import os 
import json 

# SETUP THE ENVIRONMENT
load_dotenv()
client = OpenAI()

f = open("weather_func_desc.txt","r")
weather_func_description = f.read()
f.close()

f = open("order_func_desc.txt","r")
order_func_description = f.read()
f.close()

# CREATE THE FUNCTION - GET WEATHER 
def get_weather(zipcode):
    country_code = "in"
    openweather_api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?zip={zipcode},{country_code}&appid={openweather_api_key}"
    response = requests.get(url)
    result = response.json()
    return result 

# CREATE THE FUNCTION - GET ORDER
def get_order(user_id):
    url = f"http://localhost:8000/delivery/{user_id}"
    response = requests.get(url)
    result = response.json()
    return result 

# FUNCTION BLUEPRINT / FUNCTION SCHEMA (SCHEMA IS NOT EXECUTION)
openai_tools = [
    {
        "type": "function",
        "name": "get_weather",
        "description": weather_func_description,
        "parameters": {
            "type": "object",
            "properties": {
                "zipcode": {
                    "type": "string",
                    "description": "The zipcode of the location to get the weather of."
                },
            },
            "required": ["zipcode"]
        }
    },
    {
        "type": "function",
        "name": "get_order",
        "description": order_func_description,
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The ID of the user to get the order data info of."
                },
            },
            "required": ["user_id"]
        }
    }
]

# ASK FOR CUSTOMER QUERY
user_query = input("Human Query: ")

# MAKE THE FIRST LLM CALL
response = client.responses.create(
    model="gpt-5.6-luna",
    tools=openai_tools,
    input=user_query
)

# LOGIC FOR EXECUTING THE FUNCTION
function_output = []

for item in response.output:
    if item.type == "function_call":
        arguments = json.loads(item.arguments) #str to dict 
        if item.name == "get_weather":
            result = get_weather(arguments['zipcode'])
            print("RAW FUNCTION OUTPUT")
            print(result)
            print("="*30)
        elif item.name == "get_order":
            result = get_order(arguments['user_id'])
            print("RAW FUNCTION OUTPUT")
            print(result)
            print("="*30)
        else:
            result = "unknown function called"

        function_output.append({
            "type": "function_call_output",
            "call_id": item.call_id,
            "output": json.dumps({"result": result}) #json.dumps - dict to str 
        })

# MAKE THE SECOND LLM CALL
final_response = client.responses.create(
    model="gpt-5.6-luna",
    input=function_output,
    previous_response_id=response.id
)
print("\nAI SUMMARIZED OUTPUT\n")
print(final_response.output_text)