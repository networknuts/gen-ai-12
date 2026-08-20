from dotenv import load_dotenv
from openai import OpenAI 

# STEP 1: LOAD THE .ENV FILE
load_dotenv()
human_question = input("Enter your question: ")

# STEP 2: MAKING THE REQUEST
client = OpenAI()
response = client.responses.create(
    model="gpt-5.6-luna",
    input=[
        {
            "role": "user",
            "content": "hi, my name is aryan."
        },
        {
            "role": "assistant",
            "content": "Hi Aryan! Nice to meet you. How can I help you today?"
        },
        {
            "role": "user",
            "content": human_question
        }
    ]
)

# STEP 3: PRINT OUTPUT
print(response.output_text)