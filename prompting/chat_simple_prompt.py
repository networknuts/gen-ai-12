from dotenv import load_dotenv
from openai import OpenAI 

# STEP 1: LOAD THE .ENV FILE
load_dotenv()
human_question = input("Enter your question: ")

# STEP 2: READ SYSTEM PROMPT
f = open("simple_prompt.txt","r")
SYSTEM_PROMPT = f.read()
f.close()

# STEP 3: MAKING THE REQUEST
client = OpenAI()
response = client.responses.create(
    model="gpt-5.6-luna",
    instructions=SYSTEM_PROMPT,
    input=human_question
)

# STEP 4: PRINT OUTPUT
print(response.output_text)
print("="*50)
print(response.usage)