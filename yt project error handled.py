import os
import json
import nltk
import googleapiclient.discovery
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import tkinter as tk
from tkinter import Entry, Label, Button, StringVar


# Initialize the YouTube Data API with your API key

api_key = "AIzaSyB-hv3dBbN9pCX53u3V9XHlG2ulmJigDfQ"
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

# Initialize the Sentiment Intensity Analyzer
nltk.download('vader_lexicon')
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

# Define a function to collect comments from the top two videos for each product
# Define a function to collect comments from the top two videos for each product
def collect_comments(product1, product2, max_comments=5):
    product1_comments = []
    product2_comments = []

    # Search for videos related to Product 1
    product1_search = youtube.search().list(
        q=product1,
        type="video",
        part="id",
        maxResults=1
    ).execute()

    for item in product1_search["items"]:
        video_id = item["id"]["videoId"]
        try:
            comments = get_video_comments(video_id, max_comments)
            if len(comments) < max_comments:
                print(f"Insufficient comments for video {video_id}. Skipping.")
            else:
                product1_comments.extend(comments)
        except Exception as e:
            print(f"Error while fetching comments for video {video_id}: {e}")

    # Search for videos related to Product 2
    product2_search = youtube.search().list(
        q=product2,
        type="video",
        part="id",
        maxResults=1
    ).execute()

    for item in product2_search["items"]:
        video_id = item["id"]["videoId"]
        try:
            comments = get_video_comments(video_id, max_comments)
            if len(comments) < max_comments:
                print(f"Insufficient comments for video {video_id}. Skipping.")
            else:
                product2_comments.extend(comments)
        except Exception as e:
            print(f"Error while fetching comments for video {video_id}: {e}")

    return product1_comments, product2_comments


# Create a function to update the scores and compare products
def update_scores():
    product1_name = product1_entry.get()
    product2_name = product2_entry.get()
    product1_comments, product2_comments = collect_comments(product1_name, product2_name)
    product1_score = analyze_sentiment(product1_comments)
    product2_score = analyze_sentiment(product2_comments)
    product1_final_score = map_to_0_10(product1_score)
    product2_final_score = map_to_0_10(product2_score)
    product1_output.set(f"Product 1 Score: {product1_final_score:.2f}")
    product2_output.set(f"Product 2 Score: {product2_final_score:.2f}")

    if product1_score > product2_score:
        comparison_output.set(f"The sentiment towards {product1_name} seems to be more favorable compared to {product2_name}")
    elif product2_score > product1_score:
        comparison_output.set(f"The sentiment towards {product2_name} seems to be more favorable compared to {product1_name}")
    else:
        comparison_output.set(f"The sentiment scores for {product1_name} and {product2_name} are equal")

# Create a function to map sentiment scores to a 0-10 scale
def map_to_0_10(score):
    return (score + 1) * 5


# Create the GUI window
window = tk.Tk()
window.title("Product Sentiment Analysis")

# Create input fields for product names
product1_label = Label(window, text="Product 1:")
product1_label.pack()
product1_entry = Entry(window)
product1_entry.pack()

product2_label = Label(window, text="Product 2:")
product2_label.pack()
product2_entry = Entry(window)
product2_entry.pack()

# Create a button to trigger sentiment analysis
analyze_button = Button(window, text="Analyze", command=update_scores)
analyze_button.pack()

# Create output fields for scores
product1_output = StringVar()
product2_output = StringVar()
product1_output_label = Label(window, textvariable=product1_output)
product1_output_label.pack()
product2_output_label = Label(window, textvariable=product2_output)
product2_output_label.pack()

# Create a label to display the comparison statement
comparison_output = StringVar()
comparison_label = Label(window, textvariable=comparison_output)
comparison_label.pack()

# Start the GUI application
window.mainloop()
