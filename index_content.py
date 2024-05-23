import os
import requests
import ollama
import chromadb
from bs4 import BeautifulSoup


VECTOR_DB_PATH = "./data/"
URL_COLLECTION_NAME = "documents_index"
# Can vary check documentation and play
# https://ollama.com/library/all-minilm/blobs/85011998c600
MAX_TOKENS = 4096 
EMBEDDING_MODEL = "all-minilm:latest" # use mxbai-embed-large for better results

print("API Server:" + os.environ["OLLAMA_HOST"])
urls_to_index = ["https://study.iitm.ac.in/ds/academics.html","https://study.iitm.ac.in/ds/admissions.html"]
client = chromadb.PersistentClient(path=VECTOR_DB_PATH)

def setup_database(fresh_start=False):
    collection = client.get_collection(name=URL_COLLECTION_NAME)
    if collection and fresh_start:
        client.delete_collection(name=URL_COLLECTION_NAME)


def index_url(url):
    print("====================="+url)
    # Fetch content from URL
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch URL: {url}")
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    text_content =  soup.get_text()
    # Split text into chunks of 4096 tokens
    #print("===================== Get text")
    tokens = text_content.split()
    chunks = [" ".join(tokens[i:i + MAX_TOKENS]) for i in range(0, len(tokens), MAX_TOKENS)]
    
    collection = client.get_or_create_collection(name=URL_COLLECTION_NAME)

    print("Lenght of chunks"+ str(len(chunks)))
    # Generate embeddings and store in ChromaDB
    for i, d in enumerate(chunks):
        response = ollama.embeddings(model=EMBEDDING_MODEL, prompt=d)
        embedding = response["embedding"]
        doc_id = url+"#chunk="+str(i)
        #print(doc_id)
        #print("===================== Adding Token")
        #print(embedding)
        collection.add(ids=[doc_id],embeddings=[embedding],documents=[d])


def main():
    fresh_start = False
    restart =  input("Do you want to clear existing index and resrart? Say Yes or No.:") 
    if restart.upper() == "YES":
        fresh_start = True

    # setup database
    setup_database(fresh_start=fresh_start)

    # start indexing
    for url in urls_to_index:
        index_url(url)

if __name__ == '__main__':
    main()