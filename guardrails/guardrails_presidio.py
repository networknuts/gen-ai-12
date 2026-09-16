from openai import OpenAI 
from dotenv import load_dotenv
from presidio_analyzer import AnalyzerEngine

load_dotenv()
client = OpenAI()
analyzer = AnalyzerEngine()

text = """
John Smith emailed Alice Brown.
Alice Brown told John Smith that his account was blocked.
What happened?
"""

results = analyzer.analyze(
    text=text,
    entities=["PERSON"],
    language="en"
)

# CREATE A MAPPING DICTIONARY
mapping = {}
for result in results:
    name = text[result.start:result.end]
    mapping.setdefault(name,f"PERSON_{len(mapping)+1}")

sanitized_text = text 

for name, pseudonym in mapping.items():
    sanitized_text = sanitized_text.replace(name,pseudonym)

# SEND SANITIZED DATA TO LLM
response = client.responses.create(
    model="gpt-5.6-luna",
    input=f"Explain this situation: {sanitized_text}"
)
print("LLM OUTPUT")
print(response.output_text)