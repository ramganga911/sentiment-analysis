import os
import json
import nltk
import googleapiclient.discovery
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

# Initialize the YouTube Data API with your API key
api_key = "AIzaSyB-hv3dBbN9pCX53u3V9XHlG2ulmJigDfQ"
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

# Initialize the Sentiment Intensity Analyzer

sia = SentimentIntensityAnalyzer()

# Define a function to analyze sentiment and calculate a score
def analyze_sentiment(comments):
    sentiment_scores = [sia.polarity_scores(comment)["compound"] for comment in comments]
    avg_score = sum(sentiment_scores) / len(sentiment_scores)
    return avg_score

# Define a function to collect comments from the YouTube Data API
def get_video_comments(video_id, max_results=10):
    comments = []

    results = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText",
        maxResults=max_results
    ).execute()

    for item in results["items"]:
        comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        comments.append(comment)

    return comments

# Define a function to collect comments and their sentiment scores
def collect_comments_with_scores(product_name):
    comments = get_video_comments(product_name)
    sentiment_scores = [sia.polarity_scores(comment)["compound"] for comment in comments]
    return {"Comment": comments, "Sentiment Score": sentiment_scores}

# Example usage
product_name = "0X0Jm8QValY"
data = collect_comments_with_scores(product_name)

# Create a Pandas DataFrame from the data
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
output_file = "sentiment_scores2.xlsx"
df.to_excel(output_file, index=False)

print(f"Data has been saved to {output_file}")
