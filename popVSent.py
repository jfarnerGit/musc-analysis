from lyricProcessing import *
from lyricFetching import *
from calcSentiment import *
import matplotlib.pyplot as plt

'''
Plots popularity according to genius against VADER sentiment score
'''

artist = 'David Allan Coe'
df = pd.read_csv(artist_to_csv(artist))
clean_and_tokenize(df)
calc_sentiment(df)

df['popularity'] = df.index + 1

x = df['popularity']
y = df['emotion_score']
size = df['emotion_class']

fig = plt.scatter(x,y, color = 'darkviolet')

plt.xlabel("Popularity Rank", fontweight = 'bold')
plt.ylabel('Sentiment Score', fontweight = 'bold')

plt.title(artist + " Sentiment Score vs. Popularity", fontweight = 'bold')
plt.figure(figsize = (12,4))

plt.show()
