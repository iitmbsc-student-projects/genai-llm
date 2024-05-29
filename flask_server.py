import os
from flask import Flask, request, render_template_string
from flask_cors import CORS
import search

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# HTML template
html_template = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Search Form</title>
</head>
<body>
    <form action="/search" method="post">
        <label for="query">Query:</label>
        <input type="text" id="query" name="query"><br><br>
        <input type="checkbox" id="custom_embedding" name="custom_embedding">
        <label for="custom_embedding">Use custom embedding</label><br><br>
        <button type="submit">Search</button>
    </form>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index_handler():
    return render_template_string(html_template)

@app.route('/search', methods=['POST'])
def search_handler():
    # This function will handle the search request
    # You can fill this function with your search logic
    data = request.form
    query = data.get('query')
    use_embeddings = data.get('custom_embedding', None) is not None

    answer = search.main(query, use_embeddings)

    return f"""
Received query: {query}, use custom embedding: {use_embeddings}.
<br/>
<br/>
Answer:
{answer}
"""

if __name__ == '__main__':
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=os.getenv("FLASK_PORT", 80)
    )

