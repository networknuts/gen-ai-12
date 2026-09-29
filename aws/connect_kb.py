from dotenv import load_dotenv
import boto3
import os

# SETUP THE ENVIRONMENT
load_dotenv()

# PROVIDE AWS CONFIGURATION
region = os.getenv("AWS_REGION")
kb_id = os.getenv("BEDROCK_KB_ID")
model_arn = os.getenv("BEDROCK_MODEL_ARN")
query = input("Enter human query: ")

# CONNECT TO AWS BEDROCK
client = boto3.client('bedrock-agent-runtime',region_name=region)

# GENERATE ANSWER FROM KB
response = client.retrieve_and_generate(
    input={'text':query},
    retrieveAndGenerateConfiguration={
        "type": "KNOWLEDGE_BASE",
        "knowledgeBaseConfiguration": {
            "knowledgeBaseId": kb_id,
            "modelArn": model_arn
        },
    },
)

print(response['output']['text'])

for citation in response.get("citations"):
    for reference in citation.get("retrievedReferences"):
        source_document = reference.get("location").get("s3Location").get("uri")
        if source_document:
            print(f"Source: {source_document}")