import requests
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from model.src.infer import generate_keywords

app = Flask(__name__)
CORS(app)

load_dotenv()

def search_articles(keywords):
    api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
    search_engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")

    if not api_key or not search_engine_id:
        raise ValueError("API key or Search Engine ID not found in environment variables.")

    url = "https://www.googleapis.com/customsearch/v1"
    results = []
    
    for keyword in keywords:
        params = {
            "q": keyword,
            "key": api_key,
            "cx": search_engine_id,
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            for item in data.get("items", []):
                results.append({
                    "title": item.get("title"),
                    "link": item.get("link"),
                    "snippet": item.get("snippet"),
                })
        else:
            print(f"Error: {response.status_code}, {response.text}")
    
    return results
'''
dummy_keywords = ["nuclear energy good", "nuclear energy for desalination"]
articles = search_articles(dummy_keywords)
for article in articles:
    print(f"Title: {article['title']}")
    print(f"Link: {article['link']}")
    print(f"Snippet: {article['snippet']}\n")
'''

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    topic = data.get("topic")
    side = data.get("side")
    if not topic or not side:
        return jsonify({"error": "Missing topic or side"}), 400
    
    keywords = generate_keywords(topic, side)
    articles = search_articles(keywords)
    return jsonify({"keywords": keywords, "articles": articles})

if __name__ == "__main__":
    app.run(debug=True)