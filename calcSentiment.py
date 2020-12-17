from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np
import math
from termcolor import colored

"""
These functions are used to calculate sentiment scores for each song based on lyrics using the Vader Sentiment package.

The Vader documentation indicates that the package is more reliable when used on smaller blocks of text, so each song
is split into chunks. Scores are calculated for each chunk and then averaged. 

The final scores added to the dataframe are an estimation for overall positive, negative, or neutral sentiment.

Can only be run after data is cleaned and tokenized using lyricProcessing.py.
"""

analyser = SentimentIntensityAnalyzer()

#splits songs up into 10 equal chunks
def song_chunks(lyrics):
    length = len(lyrics)
    chunks = 10
    split = []
    #for defined number of chunks, append placeholder value to array: split = ['placeholder', 'placeholder', etc...]
    for i in range(chunks):
        split.append('placeholder')
    partition_size = math.floor(length/ chunks)
    start = np.arange(0, length, partition_size)
    split = []
    for part in range(10):
        split.append(lyrics[start[part]:start[part]+partition_size])
    return split

# takes in a lyric chunk and calculates the avg sentiment score from all chunks
def sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
    return score

# uses above method to find average sentiment score of chunks
# avg sentiment score is used to label the song with labels for positive, negative, or neutral
def findAvgSentimentScore(split):
    sum = 0
    for i in split:
        x = sentiment_analyzer_scores(i)
        sum += x['compound']
    final = sum/len(split)
    fin = 0
    if final < 0:
        fin = -1
    elif final > 0 and final < 0.5:
        fin = 0.5
    else:
        fin = 1
    # print(final)
    return fin


#if you want average vader scores instead of labels, can use this as the lambda function - TODO: clean up this process
def findAvgSentimentScore2(split):
    sum = 0
    for i in split:
        x = sentiment_analyzer_scores(i)
        sum += x['compound']
    final = sum/len(split)
    return final


# Assign sentiment scores to each song based on average score from song lyric chunks using lambda functions
def calc_sentiment(df):
    chunked = lambda x: song_chunks(x)
    vader_scores = lambda x: findAvgSentimentScore2(x)
    vader_class = lambda x: findAvgSentimentScore(x) #use findAvgSentimentScore2 if you want scores
    df['chunked'] = df['tokenized_lyrics'].apply(chunked)
    df['emotion_score'] = df['chunked'].apply(vader_scores)
    df['emotion_class'] = df['chunked'].apply(vader_class)
    print(colored("Calculating Vader sentiment score... \nSongs are being classified as Positive(1.0), Neutral(0.5), or Negative(-1.0)...", 'white'))
    print(colored("Added column to Dataframe: 'emotion_score'\n", 'yellow'))
    print(colored("Added column to Dataframe: 'emotion_class'\n", 'yellow'))
