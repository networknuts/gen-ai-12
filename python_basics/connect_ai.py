import requests
from dotenv import load_dotenv
import os 
import json

# STEP 0: ASK FOR HUMAN QUESTION
query = input("Human Query: ")

# STEP 1: LOAD THE .ENV FILE
load_dotenv()

# STEP 2: DECLARE THE OPENAI API KEY VARIABLE
OPENAI_API_KEY = os.getenv("OPENAI_APIKEY")

# STEP 3: SET THE OPENAI URL
OPENAI_URL = "https://api.openai.com/v1/responses"

# STEP 4: ASSIGN HEADERS
OPENAI_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}"
}

# STEP 5: DEFINE THE PAYLOAD
OPENAI_DATA = {
    "model": "gpt-5.6-luna",
    "input": query
}

# STEP 6: EXECUTE THE HTTP POST REQUEST
response = requests.post(OPENAI_URL,headers=OPENAI_HEADERS,data=json.dumps(OPENAI_DATA))
print(response.json()['output'][0]['content'][0]['text'])