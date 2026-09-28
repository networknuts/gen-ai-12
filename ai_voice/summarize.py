from dotenv import load_dotenv
from openai import OpenAI 

# SETUP THE ENVIRONMENT
load_dotenv()
client = OpenAI()

SYSTEM_PROMPT = """
You are an AI meeting notes assistant.
You will receieve raw meeting data containing
interruptions, filler words and other common speech-to-text issues.

Please convert this raw data into a professional meeting summary
which can be shared with relevant stakeholders.
"""

def summarize(raw_file,polished_file):
    f = open(raw_file,"r")
    raw_data = f.read()
    response = client.responses.create(
        model="gpt-6-luna",
        instructions=SYSTEM_PROMPT,
        input=raw_data
    )
    f.close()
    with open(polished_file,"w") as polished_file_path:
        polished_file_path.write(response.output_text)
    print("Meeting summary generated.")


summarize("raw_meeting.txt","summary.txt")