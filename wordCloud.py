import numpy as np
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from lyricProcessing import *
from lyricFetching import *

'''
Quick script to generate wordclouds in any shape. Don't like wordclouds, so think this is a one off. No plans to
tie this into automation sequence
'''
artist = 'Johnny Cash'

#Mask defines the shape of the word cloud
#Make sure that orginal image is a silhouette with very defined shapes for best effect
#Convert images to silhouettes using Photoshop or browser tools like Canva
mask = np.array(Image.open('filename.png/jpg'))

wc = WordCloud(width = 1600, height = 1600, background_color="white",  mask=mask,
               stopwords=STOPWORDS, contour_width=0, contour_color='black')

df = pd.read_csv(artist_to_csv(artist))
clean_and_tokenize(df)

bag_of_words = ''

for i in df['cleaned_lyrics']:
    bag_of_words = bag_of_words + ' '+i

print(bag_of_words)
plt.figure(figsize=[10,10])

wordcloud = wc.generate(bag_of_words)
image_colors = ImageColorGenerator(mask)


plt.imshow(wordcloud, interpolation='bilinear')
plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")

plt.axis("off")
plt.savefig("JohnnyCash.png", format="png")
plt.show()
