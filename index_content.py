import os
import requests
import ollama
import chromadb
from bs4 import BeautifulSoup
import logging

VECTOR_DB_PATH = "./data/"
COLLECTION_NAME = "documents_index"
MAX_TOKENS = 4096
EMBEDDING_MODEL = "all-minilm:latest"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("API Server:" + os.environ.get("OLLAMA_HOST", "Not set"))
urls_to_index = ["https://study.iitm.ac.in/ds/academics.html","https://study.iitm.ac.in/ds/admissions.html"]
client = chromadb.PersistentClient(path=VECTOR_DB_PATH)

def random_id():
    from uuid import uuid4
    return uuid4().hex

def setup_database(fresh_start=False):
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    if collection and fresh_start:
        client.delete_collection(name=COLLECTION_NAME)
        logger.info("Deleted existing collection.")

def index(text_content):
    tokens = text_content.lower().split()
    chunks = [" ".join(tokens[i:i + MAX_TOKENS]) for i in range(0, len(tokens), MAX_TOKENS)]
    
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    logger.info(f"Number of chunks: {len(chunks)}")
    for i, d in enumerate(chunks):
        try:
            response = ollama.embeddings(model=EMBEDDING_MODEL, prompt=d)
            embedding = response["embedding"]
            doc_id = random_id()
            collection.add(ids=[doc_id], embeddings=[embedding], documents=[d])
            logger.info(f"Indexed chunk {i+1}/{len(chunks)}")
        except Exception as e:
            logger.error(f"Error indexing chunk {i+1}: {e}")

def main():
    fresh_start = input("Do you want to clear existing index and restart? Say Yes or No.:")
    setup_database(fresh_start=fresh_start.upper() == "YES")

    # Start indexing
    index(open('train.txt').read())

if __name__ == '__main__':
    main()

