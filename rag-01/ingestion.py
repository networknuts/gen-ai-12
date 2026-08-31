from langchain_opendataloader_pdf import OpenDataLoaderPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv 
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

# ENVIRONMENT VARIABLES
load_dotenv()
PDF_FILE_PATH = "large_data.pdf"
EMBEDDING_MODEL = "text-embedding-3-large"
QDRANT_URL = "http://localhost:6333"
QDRANT_COLLECTION_NAME = "tech_collection"

# STEP 1: LOAD THE PDF INTO TEXT
loader = OpenDataLoaderPDFLoader(
    file_path=PDF_FILE_PATH,
    format="text",
    quiet=True
)
pdf_text_data = loader.load()
print("PDF LOADED SUCCESSFULLY")

# STEP 2: CHUNKING STRATEGY
text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
chunked_data = text_splitter.split_documents(pdf_text_data)
print("CHUNKING COMPLETED")

# STEP 3: EMBEDDING STRATEGY
embeddings = OpenAIEmbeddings(
    model=EMBEDDING_MODEL
)

# STEP 4: STORE CHUNKS IN VECTOR DATABASE
qdrant = QdrantVectorStore.from_documents(
    chunked_data,
    embeddings,
    url=QDRANT_URL,
    prefer_grpc=False,
    collection_name=QDRANT_COLLECTION_NAME,
)
print("SAVED TO VECTOR DATABASE")