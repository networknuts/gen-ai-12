from dotenv import load_dotenv
from openai import OpenAI 

# STEP 1: LOAD THE .ENV FILE
load_dotenv()
human_question = input("Enter your question: ")

# STEP 2: MAKING THE REQUEST
client = OpenAI()
response = client.responses.create(
    model="gpt-5.6-luna",
    input=human_question
)

# STEP 3: PRINT OUTPUT
print(response.output_text)