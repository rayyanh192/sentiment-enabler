from flask import Flask, request, jsonify
from flask_cors import CORS
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer

app = Flask(__name__)
CORS(app)


embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
kw_model = KeyBERT(model=embedding_model)

@app.route('/keywords', methods=['POST'])
def extract_keywords():
    data = request.json
    topic = data.get('topic', '')

    if not topic:
        return jsonify({"error": "Topic is required"}), 400

    try:
        # Single prompt that includes both perspectives
        combined_prompt = (
            f"Provide keywords for two opposing perspectives on the topic '{topic}':\n"
            "1. Perspective supporting individual freedoms, personal autonomy, and rights.\n"
            "2. Perspective focusing on protection, preservation, and moral responsibility."
        )

        # Extract keywords from the combined prompt
        extracted_keywords = kw_model.extract_keywords(
            combined_prompt,
            keyphrase_ngram_range=(2, 3),
            stop_words='english',
            top_n=10  # Extract more keywords to split between perspectives
        )

        # Split the extracted keywords into two sets
        midpoint = len(extracted_keywords) // 2
        pro_choice_keywords = [kw[0] for kw in extracted_keywords[:midpoint]]
        pro_life_keywords = [kw[0] for kw in extracted_keywords[midpoint:]]

        return jsonify({
            "topic": topic,
            "pro_choice_keywords": pro_choice_keywords,
            "pro_life_keywords": pro_life_keywords
        })

    except Exception as e:
        print("Error during keyword extraction:", e)
        return jsonify({"error": "An error occurred while extracting keywords"}), 500


@app.route('/scrape', methods=['POST'])
def scrape_articles():
    data = request.json
    keywords = data.get('keywords', [])

    if not keywords:
        return jsonify({"error": "No keywords provided for scraping"}), 400

    articles = []
    for keyword in keywords:
        articles.append({"title": f"Article about {keyword}", "url": "https://example.com/article1"})

    return jsonify({"articles": articles})

# Placeholder: Sentiment analysis logic
@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    data = request.json
    articles = data.get('articles', [])
    # Simulated sentiment analysis
    sentiments = [
        {"title": articles[0]["title"], "sentiment": "neutral"},
        {"title": articles[1]["title"], "sentiment": "positive"}
    ]
    print("Returning sentiments:", sentiments)
    return jsonify({"sentiments": sentiments})

# Placeholder: AI-generated summary
@app.route('/summary', methods=['POST'])
def generate_summary():
    data = request.json
    articles = data.get('articles', [])
    # Simulated summary generation
    summary = "This is a summary paragraph combining key points from the articles."
    print("Returning summary:", summary)
    return jsonify({"summary": summary})

if __name__ == '__main__':
    app.run(debug=True)