import lyricsgenius as genius
import os
import json
import pandas as pd

"""
This Program generates csv files containing the lyrics from a set number of songs by a given artist. 
Call create_csv in for loop for list of artists with defined song value to fetch multiple at once.
Any connection interrupts cause program to abort (for now), so recommend doing one artist at a time. 

Songs are added in order of popularity ranked by Genius.com
"""

#TODO: input your own credentials
geniusCreds = "ENTER CREDENTIALS"
api = genius.Genius(geniusCreds)

#Console input for artist name
def get_artist_name():
    artist_name = input("Enter Artist: ")
    return artist_name

#Console input for number of songs
def get_num_songs():
    num_songs = int(input("Enter Num Songs: "))
    return num_songs

#Fetch all data for artist's songs and save as JSON
def fetch_genius_data(artist_name, num_songs):
    artist = api.search_artist(artist_name, max_songs = num_songs)
    artist.save_lyrics()

#Pull data from JSON and place into new dataframe
def convert_to_df(artist_name):
    artist_name_clean = artist_name.replace(' ', '')
    file_name = 'Lyrics_' + artist_name_clean + '.json'
    current_path = os.getcwd()
    lyric_path = current_path + file_name
    with open(file_name) as json_data:
        data = json.loads(json_data.read())
        songs = data.get('songs')
        lyric_df = pd.DataFrame(columns=['artist', 'song_name', 'lyrics', 'release', 'genius_url']) #can add features
        for x in songs:
            lyric_df = lyric_df.append({
                'artist': artist_name,
                'song_name': x.get('title'),
                'lyrics': x.get('lyrics'),
                'release': x.get('release_date'),
                'genius_url': x.get('url'),
                #TODO: get albums working - issue is with nested JSON being in List format
                #'album': x.get('album')
            }, ignore_index = True)
    return lyric_df

#Function to combine previous functions - gets user from 0 data to uncleaned dataframe
def build_dataframe():
    a = get_artist_name()
    b = get_num_songs()
    fetch_genius_data(a, b)
    return (convert_to_df(a))

#Converts dataframe to csv and save file - can import csv as dataframe for any later work.
def artist_to_csv(artist_name):
    artist_name_clean = artist_name.replace(' ', '')
    artist_name_clean = artist_name_clean.lower()
    csv_name = artist_name_clean + '_lyrics' + '.csv'
    return csv_name

#Combines all previous functions - go from 0 data to csv
def create_csv():
    df = build_dataframe()

    artist_name = df['artist'][1]
    artist_name_clean = artist_name.replace(' ', '')
    artist_name_clean = artist_name_clean.lower()
    current_path = os.getcwd()
    csv_name = artist_name_clean + '_lyrics' + '.csv'

    #csv_path = current_path + csv_name

    df.to_csv(csv_name)

#Uncomment to test - otherwise import and call create_csv() in other scripts
#create_csv()
