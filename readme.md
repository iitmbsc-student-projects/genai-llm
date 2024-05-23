# Simple LLM Based Search


## Setup Ollama and Models
1. Install [Ollama](https://ollama.com/download)
2. Download the model - we are getting [tinyllama](https://ollama.com/library/tinyllama) which is a very compact model. And it should run on most machines.
    - `ollama pull tinyllama:latest`
3. Download model for creating embeddings. The [all-minilm](https://ollama.com/library/all-minilm) aims to train sentence embedding models on very large sentence level datasets using a self-supervised contrastive learning objective.
    - `ollama pull all-minilm:latest`
4. Start, and make sure ollama is available at [http://localhost:11434/](http://localhost:11434/)

5. Install the packages in requirements.ttx
6. Run indexing
    `export OLLAMA_HOST='0.0.0.0';python index_content.py`
7. Test searching
    `export OLLAMA_HOST='0.0.0.0';python search.py `
8. Play around by changing the models and other parameters

