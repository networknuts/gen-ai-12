from dotenv import load_dotenv
from openai import OpenAI 

# STEP 1: LOAD THE .ENV FILE
load_dotenv()
code_to_be_judged = open("code.txt","r")
USER_CODE = code_to_be_judged.read()
code_to_be_judged.close()

# STEP 2: READ SYSTEM PROMPT
f = open("cot.txt","r")
SYSTEM_PROMPT = f.read()
f.close()

# STEP 3: MAKING THE REQUEST
client = OpenAI()
response = client.responses.create(
    model="gpt-5.6-luna",
    instructions=SYSTEM_PROMPT,
    reasoning={"effort": "medium"},
    input=USER_CODE
)

# STEP 4: PRINT OUTPUT
print(response.output_text)
print("="*50)
print(response.usage)