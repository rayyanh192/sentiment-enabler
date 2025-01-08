import requests
from dotenv import load_dotenv
import os

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

dummy_keywords = ["climate change fake", "renewable energy initiatives"]
articles = search_articles(dummy_keywords)
for article in articles:
    print(f"Title: {article['title']}")
    print(f"Link: {article['link']}")
    print(f"Snippet: {article['snippet']}\n")