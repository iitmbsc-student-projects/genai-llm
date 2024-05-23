import requests
import ollama
import chromadb


VECTOR_DB_PATH = "./data/"
URL_COLLECTION_NAME = "documents_index"
MAX_TOKENS = 4096 # https://inference.readthedocs.io/en/latest/models/builtin/llm/tiny-llama.html
MAX_EMBEDDING_RESULTS = 1
ANSWER_MODEL = "tinyllama::latest" # use llama2 for better
EMBEDDING_MODEL = "all-minilm:latest" # use mxbai-embed-large for better results
print("API Server:" + os.environ["OLLAMA_HOST"])


client = chromadb.PersistentClient(path=VECTOR_DB_PATH)


def search_index(query):
    print("Query:"+query)
    response = ollama.embeddings(model=EMBEDDING_MODEL, prompt=query)
    embedding = response["embedding"]        
    collection = client.get_or_create_collection(name=URL_COLLECTION_NAME)
    results = collection.query(query_embeddings=[embedding],n_results=MAX_EMBEDDING_RESULTS)
    # print(results)
    data = ""
    for data_part in results['documents'][0]:
        data = data + data_part[0]

    return data


def answer(data, query):
    output = ollama.generate(
      host = API_HOST,
      model=ANSWER_MODEL,
      prompt=f"Using this data: {data}. Respond to this prompt: {query}"
    )
    print("===============================================")
    print(output['response'])
    print("===============================================")

def main(query):
    data = search_index(query)
    # print("data:"+ data)
    answer(data, query)    

if __name__ == '__main__':
    # query = input("Ask:")
    query = "Who can apply for admission?"
    main(query)