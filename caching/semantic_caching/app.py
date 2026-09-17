from dotenv import load_dotenv
from openai import OpenAI 
import redis
import hashlib
import uuid 
from qdrant_client import QdrantClient, models

# SETUP THE ENVIRONMENT
load_dotenv()
openai = OpenAI()
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)
qdrant = QdrantClient(url="http://localhost:6333")
COLLECTION = "cache"

# STEP 1: CREATE QDRANT COLLECTION IF IT DOES NOT EXIST
def init_qdrant():
    if not qdrant.collection_exists(COLLECTION):
        qdrant.create_collection(
            collection_name=COLLECTION,
            vectors_config=models.VectorParams(
                size=1536,
                distance=models.Distance.COSINE
            )
        )

# STEP 2: CONVERT USER QUESTION INTO REDIS KEY
def convert_hash(prompt: str):
    normalized_prompt = prompt.strip().lower()
    hashed = hashlib.sha256(normalized_prompt.encode()).hexdigest()
    return f"cache:{hashed}"

# STEP 3: CREATE EMBEDDING
def get_embedding(text: str):
    response = openai.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

# STEP 4: ASK LLM FOR RESPONSE
def ask_llm(prompt: str):
    response = openai.responses.create(
        model="gpt-5.6-luna",
        input=prompt
    )
    return response.output_text

# STEP 5: SEARCH QDRANT FOR SIMILAR QUERY
def search_qdrant(embedding):
    result = qdrant.query_points(
        collection_name=COLLECTION,
        query=embedding,
        limit=1
    )
    if result.points and result.points[0].score > 0.8:
        return result.points[0].payload["answer"]
    else:
        return None 

# STEP 6: SAVE QUERY + ANSWER TO QDRANT FOR FUTURE
def save_to_qdrant(prompt,embedding,answer):
    qdrant.upsert(
        collection_name=COLLECTION,
        points=[
            models.PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "prompt": prompt,
                    "answer": answer 
                }
            )
        ]
    )

# STEP 7: GET ANSWER USING ABOVE LOGIC
def get_answer(prompt):
    # 1. CONVERT PROMPT TO KEY AND SEARCH REDIS
    key = convert_hash(prompt)
    answer = redis_client.get(key)
    if answer:
        print("REDIS CACHE HIT")
        return answer
    # 2. SEMANTIC SEARCH IN QDRANT 
    embedding = get_embedding(prompt)
    answer = search_qdrant(embedding)
    if answer:
        print("QDRANT CACHE HIT")
        #3. SAVING ANSWER TO REDIS
        redis_client.set(key,answer)
        return answer
    # 4. INVOKING LLM CALL
    print("INVOKING LLM CALL")
    answer = ask_llm(prompt)
    #5. SAVE TO REDIS
    redis_client.set(key,answer)
    #6. SAVE TO QDRANT
    save_to_qdrant(prompt,embedding,answer)
    return answer 

# EXECUTE WORKFLOW
init_qdrant()

query = input("Human Query: ")
print("\nAI RESPONSE\n")
print(get_answer(query))