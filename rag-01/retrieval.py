from dotenv import load_dotenv
from openai import OpenAI 
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

# SETUP THE ENVIRONMENT
load_dotenv()
client = OpenAI()

EMBEDDING_MODEL = "text-embedding-3-large"
QDRANT_URL = "http://localhost:6333"
QDRANT_COLLECTION_NAME = "tech_collection"

embeddings = OpenAIEmbeddings(
    model=EMBEDDING_MODEL
)

# STEP 1: CONNECT TO VECTOR DATABASE
qdrant = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    collection_name=QDRANT_COLLECTION_NAME,
    url=QDRANT_URL,
)

# STEP 2: ASK FOR CUSTOMER QUERY
human_query = input("Human Query: ")

# STEP 3: PERFORM SIMILARITY SEARCH
search_results = qdrant.similarity_search(human_query)

# STEP 4: BUILDING THE CONTEXT
context = []
for chunk in search_results:
    chunk_block = f"""
    Page Content:
    {chunk.page_content}
    Page Number:
    {chunk.metadata.get("page","N/A")}
    """
    context.append(chunk_block)

# STEP 5: SYSTEM PROMPT FOR RAG
SYSTEM_PROMPT = f"""
You are an AI RAG assistant.
You have been provided content extracted from PDF document(s).
Each section includes:
- Page Content
- Page Number

Answer the user's question using only this provided information.
If the answer is available:
- Respond only from the data you have 
- Mention the relevant page number(s) from where the data came from

If the answer is not available:
- State to the user that the answer is beyond your knowledge base

Data:
{context}
"""

# STEP 6: GENERATE THE LLM RESPONSE
response = client.responses.create(
    model="gpt-5.6-luna",
    input=human_query,
    instructions=SYSTEM_PROMPT
)

print(response.output_text)