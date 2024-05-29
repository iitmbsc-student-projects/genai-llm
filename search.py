import requests
import ollama
import chromadb
import os
import logging

USE_EMBEDDINGS = True
VECTOR_DB_PATH = "./data/"
URL_COLLECTION_NAME = "documents_index"
MAX_TOKENS = 4096
MAX_EMBEDDING_RESULTS = 5  # Increased number of results for more leniency
ANSWER_MODEL = "tinyllama:latest"
EMBEDDING_MODEL = "all-minilm:latest"
SIMILARITY_THRESHOLD = 0.7  # Custom similarity threshold (adjust as needed)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("API Server:" + os.environ.get("OLLAMA_HOST", "Not set"))

client = chromadb.PersistentClient(path=VECTOR_DB_PATH)

def search_index(query):
    if not USE_EMBEDDINGS:
        logging.info("Not using any embeddings")
        return ""
    # logger.info(f"Query: {query}")
    try:
        response = ollama.embeddings(model=EMBEDDING_MODEL, prompt=query.lower())
        embedding = response["embedding"]
        collection = client.get_or_create_collection(name=URL_COLLECTION_NAME)
        results = collection.query(query_embeddings=[embedding], n_results=MAX_EMBEDDING_RESULTS)
        results = [r[0] for r in results["documents"]]
        breakpoint()

        if results:
            return " ".join(results)
        else:
            logger.info("No search results found above the similarity threshold.")
            return ""
    except Exception as e:
        logger.error(f"Error during search: {e}")
        return ""

def answer(data, query):
    if data:
        prompt = f"""
            According to this data:

            {data}

            ---
            (end of data)
            and absolutely nothing else at all, tell me {query}.

            Remember - only answer my question using the above data. do not use any other information you may have learned from anywhere else.
        """
    else:
        prompt = query
    try:
        breakpoint()
        output = ollama.generate(
            model=ANSWER_MODEL,
            prompt=prompt
        )
        response = output.get('response', '')
        logger.debug(f"Generated response: {response}")
        print()
        print("===============================================")
        print(response)
        print("===============================================")
        print()
    except Exception as e:
        logger.error(f"Error generating response: {e}")

def main(query):
    data = search_index(query)
    answer(data, query)

if __name__ == '__main__':
    USE_EMBEDDINGS = os.getenv("USE_EMBEDDINGS", "yes") == "yes"
    query = os.getenv("QUERY")
    if not query:
        query = input("Ask: ").strip()
    main(query)

