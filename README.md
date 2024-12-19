# Sentiment Enabler

Sentiment Enabler is a web application that helps users explore controversial topics by providing insights into different perspectives. Users can input a topic, and the app returns keywords, relevant articles, sentiment analysis, and a summary of the topic from opposing viewpoints (e.g., pro-choice vs. pro-life).

## Features
	•	Accepts any topic input from the user.
	•	Extracts keywords for opposing viewpoints using KeyBERT.
	•	Scrapes dummy or real articles based on keywords.
	•	Analyzes sentiment of articles.
	•	Generates a concise summary using AI.

## Tech Stack

### Backend
	•	Flask: Used for the backend REST API.
	•	KeyBERT: For keyword extraction.
	•	Sentence Transformers: For embedding generation (KeyBERT).
	•	Flask-CORS: To enable communication between the frontend and backend.

### Frontend
	•	HTML/CSS/JavaScript: For the user interface.

### API Endpoints

1. /keywords
	•	Method: POST
	•	Input:

{
  "topic": "abortion"
}


	•	Output:

{
  "topic": "abortion",
  "pro_choice_keywords": ["reproductive rights", "personal autonomy", "healthcare access"],
  "pro_life_keywords": ["sanctity of life", "unborn child", "moral responsibility"]
}



2. /scrape
	•	Method: POST
	•	Input:

{
  "keywords": ["reproductive rights", "healthcare access"]
}


	•	Output:

{
  "articles": [
    {"title": "Article about reproductive rights", "url": "https://example.com/article1"},
    {"title": "Article about healthcare access", "url": "https://example.com/article2"}
  ]
}



3. /analyze
	•	Method: POST
	•	Input:

{
  "articles": [
    {"title": "Article about reproductive rights", "url": "https://example.com/article1"}
  ]
}


	•	Output:

{
  "sentiments": [
    {"title": "Article about reproductive rights", "sentiment": "positive"}
  ]
}



4. /summary
	•	Method: POST
	•	Input:

{
  "articles": [
    {"title": "Article about reproductive rights", "url": "https://example.com/article1"}
  ]
}


	•	Output:

{
  "summary": "The articles discuss reproductive rights and the ethical considerations involved."
}

## Setup and Installation

1. Clone the Repository

git clone https://github.com/rayyanh192/sentiment-enabler.git
cd sentiment-enabler

2. Set Up the Backend
	1.	Install Python dependencies:

pip install -r requirements.txt


	2.	Start the Flask server:

python app.py



3. Serve the Frontend

Use Python’s HTTP server to serve the frontend:

cd frontend
python -m http.server 8000

Visit the frontend at: http://localhost:8000

## Folder Structure

sentiment-enabler/
├── backend/
│   ├── app.py                # Flask backend
│   ├── requirements.txt      # Python dependencies
├── frontend/
│   ├── index.html            # Frontend HTML
│   ├── style.css             # Frontend styles
│   ├── script.js             # Frontend JavaScript
└── README.md                 # Project documentation

Future Features
	•	Implement real web scraping for articles using libraries like BeautifulSoup.
	•	Add database support to store user queries and results.
	•	Integrate more advanced AI models for summarization (e.g., OpenAI GPT).

Contributing
	1.	Fork the repository.
	2.	Create a new branch:

git checkout -b feature-branch


	3.	Commit your changes:

git commit -m "Add feature"


	4.	Push to your branch:

git push origin feature-branch


	5.	Open a pull request.

## License

This project is licensed under the MIT License. See LICENSE for more information.

## Contact

Created by Rayyan Hussain
Email: rayyanhussain2024@gmail.com
GitHub: https://github.com/rayyanh192