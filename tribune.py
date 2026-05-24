import requests
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    scores = analyzer.polarity_scores(text)
    
    return scores['compound']

url = "https://tribune.com.pk/business"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
    }

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")

headlines = soup.find_all("h2")

total_score = 0
count = 0

for headline in headlines:
    score = get_sentiment(headline.get_text()) # Get the sentiment score for the headline text
    
    if len(headline.get_text().strip()) < 4 or "Sponsored" in headline.get_text():
        continue 
    
    total_score += score
    count += 1
    
    if score >= 0.05:
        sentiment = "Positive"
    elif score <= -0.05:
        sentiment = "Negative"  
    else:
        sentiment = "Neutral"
    
    print(f"Headline: {headline.get_text().strip()}") # Print the headline text instead of the headline object
    print(f"Sentiment: {sentiment}")
    print(f"Sentiment Score: {score}")
    print("-" * 50)
    
total_headlines = len(headlines)
average_score = total_score / count if count > 0 else 0
print(f"Total Headlines: {total_headlines}")
print(f"Average Sentiment Score: {average_score}")
