import pandas as pd
from lyricProcessing import *
from lyricFetching import *
from calcSentiment import *
import matplotlib.pyplot as plt
import seaborn as sns

'''
Checks lyric references over time for an artists discography. Plots information as well as heatmap to gain better 
insight into what is being counted. 
'''

artist = 'Johnny Cash'


df = pd.read_csv(artist_to_csv(artist))
clean_and_tokenize(df)




df['year'] = pd.DatetimeIndex(df['release']).year
df['wordcount'] = df['cleaned_lyrics'].str.split().str.len()

#Creating lexicons of words that trigger a reference counter - Not a super scientific solution and am reevaluating how these should be formed

#reli_s = 'spirit|god|godly|faith|jesus|lord|heaven|bible|christ|church|holy|soul|heavenly|idol|church|almighty'
death_s = 'death|demise|dying|end|passing on|passed away|loss|life|expiry|expiration|kill|murder|succumb|grave|gone'
lonely_s = 'lonely|alone|isolated|outcast|forsaken|lonesome'
vices_s = 'drinking|drinkin|alcohol|whiskey|cigarettes|smoking|cig'
sad_s = 'sad|sadness|misery|miserable|sorrow|sorrowful|despair|deject|dejected|blue|cry'

#violence_s = 'gun|shot|big iron|fight'


#reli = df.groupby('year').apply(lambda x: x['cleaned_lyrics'].str.count(reli_s).sum()/x['wordcount'].sum())
death = df.groupby('year').apply(lambda x: x['cleaned_lyrics'].str.count(death_s).sum()/x['wordcount'].sum())
lonely = df.groupby('year').apply(lambda x: x['cleaned_lyrics'].str.count(lonely_s).sum()/x['wordcount'].sum())
vices = df.groupby('year').apply(lambda x: x['cleaned_lyrics'].str.count(vices_s).sum()/x['wordcount'].sum())
sadness = df.groupby('year').apply(lambda x: x['cleaned_lyrics'].str.count(sad_s).sum()/x['wordcount'].sum())


#Plot references over time
fig = plt.figure()
ax = fig.add_subplot(111)
fig.set_facecolor('white')
ax.set_facecolor('white')

#ax.plot(reli, 'y', label = 'Religious References')
ax.plot(death, 'darkslategrey', label = 'Death References', linewidth = 3)
ax.plot(lonely, 'aquamarine', label = 'Loneliness References', linewidth = 3)
ax.plot(vices, 'royalblue', label = 'Vices References', linewidth = 3)
ax.plot(sadness, 'fuchsia', label = 'Sadness References', linewidth = 3)

plt.title(artist + ' Lyrical References', weight = 'bold')
plt.xlabel('Release Years', weight = 'bold')
plt.ylabel('References in Relation to All Lyrics', weight = 'bold')

ax.set_yticklabels(['{:,.2%}'.format(x) for x in ax.get_yticks()])
legend = ax.legend()
for line in legend.get_lines():
    line.set_linewidth(5)


plt.show()

#Plot heatmap of informative features from lexicon
keys_long = [sad_s, death_s, lonely_s, vices_s]
index = []
data_oc, data_wc = [], []
for keys_short in keys_long:
    keys = keys_short.split('|')
    for key in keys:
        key = ' ' + key + ' '
        index.append(key)
        data_oc.append(df.groupby('year').apply(lambda x: x['cleaned_lyrics'].str.contains(key).sum() / x.shape[0] * 100))
        data_wc.append(df.groupby('year').apply(lambda x: x['cleaned_lyrics'].str.count(key).sum() / x['wordcount'].sum()  * 100))
heatmap_df_oc = pd.DataFrame(data_oc, index=index, columns=df.groupby('year').groups.keys())
heatmap_df_wc = pd.DataFrame(data_wc, index=index, columns=df.groupby('year').groups.keys())

fig = plt.figure(figsize=(20,10))
ax1 = fig.add_subplot(121)
ax1 = sns.heatmap(heatmap_df_oc, ax=ax1, cmap='viridis', cbar_kws = {'format': '%.2f%%'})
ax1.set_title('Percentage of songs containing a word')
ax2 = fig.add_subplot(122)
ax2.set_title('Percentage of overall word occurrence in a year')
ax2 = sns.heatmap(heatmap_df_wc, ax=ax2, cmap='viridis', cbar_kws = {'format': '%.2f%%'})


plt.show()



