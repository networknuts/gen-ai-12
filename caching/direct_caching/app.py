from dotenv import load_dotenv
from openai import OpenAI 
import redis
import hashlib

# SETUP THE ENVIRONMENT
load_dotenv()
client = OpenAI()

# SETUP THE REDIS CONNECTION
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

# STEP 1: CREATE A HASHING STRATEGY
def convert_hash(prompt: str):
    normalized_prompt = prompt.strip().lower()
    hashed = hashlib.sha256(normalized_prompt.encode()).hexdigest()
    return f"cache:{hashed}"


# STEP 2: GENERATE THE LLM RESPONSE
def ask_llm(prompt: str):
    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt
    )
    return response.output_text

# STEP 3: MAIN CACHING LOGIC
def get_response(prompt: str):
    key = convert_hash(prompt)
    cached_output = redis_client.get(key)
    if cached_output:
        print("FOUND RESPONSE IN REDIS CACHE")
        return cached_output
    else:
        print("INVOKING LLM CALL")
        answer = ask_llm(prompt)
        redis_client.set(key,answer)
        return answer 

query = input("Human Query: ")
print("\nAI RESPONSE\n")
print(get_response(query))