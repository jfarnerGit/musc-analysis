from termcolor import colored
import re
import nltk
import pandas as pd

"""
Functions to clean and tokenize csv files created via lyricFetching.py
Removes labels to return new dataframe column: 'cleaned_lyrics'
Tokenizes cleaned lyrics to return new column: 'tokenized_lyrics'
"""

#Remove song labels like [verse], [chorus], etc, as well as new line formatting
def remove_labels(txt):
    txt = re.sub(r'[\(\[].*?[\)\]]', '', txt)
    txt = txt.replace('\n', ' ')
    return txt


#Tokenize cleaned lyrics via NLTK
def tokenize_lyrics(txt):
    re.sub("'", "", txt)

    # tokenizing text
    tokens = nltk.word_tokenize(txt)
    tokens = [w.lower() for w in tokens]

    # removing punctuation from each word
    import string
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]

    # remove remaining tokens that are not alphabetic
    words = [word for word in stripped if word.isalpha()]

    # filter out stop words
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]
    cleaned_row = [''.join(t) for t in words]
    cleaned_row = str(cleaned_row)
    return cleaned_row

#Apply remove_labels as lambda function to every row in dataframe. Outputs progress updates in console
def cleaner(df):
    label_remover = lambda x: remove_labels(x)
    print(colored("Removing song structure markers from lyrics...",'white'))
    df['cleaned_lyrics'] = df['lyrics'].apply(label_remover)
    print(colored("Added column to Dataframe: 'cleaned_lyrics' \n", 'yellow'))

#Apply tokenize_lyrics as lambda function to every row in dataframe. Outputs progress updates in console
def tokenizer(df):
    #tokenizes cleaned lyrics for NLP processing
    tokenizer = lambda x: tokenize_lyrics(x)
    print(colored("Tokenizing cleaned lyrics using NLTK... ", 'white'))
    df['tokenized_lyrics'] = df['cleaned_lyrics'].apply(tokenizer)
    print(colored("Added column to Dataframe: 'tokenized_lyrics' \n", 'yellow'))

#Combine lambda functions to produce both new columns
def clean_and_tokenize(df):
    cleaner(df)
    tokenizer(df)

