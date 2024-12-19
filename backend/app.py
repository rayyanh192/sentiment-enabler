from flask import Flask, request, jsonify
from flask_cors import CORS
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer

app = Flask(__name__)
CORS(app)


# Load KeyBERT with a high-quality embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
kw_model = KeyBERT(model=embedding_model)

@app.route('/keywords', methods=['POST'])
def extract_keywords():
    data = request.json
    topic = data.get('topic', '')

    if not topic:
        return jsonify({"error": "Topic is required"}), 400

    try:
        # Dynamic and generalized prompts
        pro_choice_text = f"The pro-choice perspective on {topic} focuses on supporting individual freedoms, personal autonomy, and the right to make decisions related to {topic}. It often emphasizes rights, choice, and access to necessary resources."
        pro_life_text = f"The pro-life perspective on {topic} centers around the protection, preservation, and sanctity of life. It often emphasizes moral responsibility, ethical considerations, and opposing actions that may harm life related to {topic}."

        # Extract keywords with KeyBERT
        pro_choice_keywords = kw_model.extract_keywords(
            pro_choice_text,
            keyphrase_ngram_range=(2, 3),  # Extract 2-3 word phrases
            stop_words='english',
            top_n=5
        )
        pro_life_keywords = kw_model.extract_keywords(
            pro_life_text,
            keyphrase_ngram_range=(2, 3),
            stop_words='english',
            top_n=5
        )

        # Clean the extracted keywords
        pro_choice_keywords = [kw[0] for kw in pro_choice_keywords]
        pro_life_keywords = [kw[0] for kw in pro_life_keywords]

        return jsonify({
            "topic": topic,
            "pro_choice_keywords": pro_choice_keywords,
            "pro_life_keywords": pro_life_keywords
        })

    except Exception as e:
        print("Error during keyword extraction:", e)
        return jsonify({"error": "An error occurred while extracting keywords"}), 500


# Placeholder: Web scraping logic
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