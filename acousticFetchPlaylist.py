import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time
sleep_min = 2
sleep_max = 5
start_time = time.time()
request_count = 0

'''
Had a couple of issues in fetching data for incorrect artist via search through spotipy. While I figure out a way to automate 
artist verification, I'm using this to fetch data based on playlists containing an artists discography. 
'''

#Insert credentials here
client_id = 'Client ID string'
client_secret = 'Client Secret string'

#authorize spotify access
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret = client_secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

username = "enter username"
playlist_id = "enter playlist id"



def analyze_playlist(creator, playlist_id):
    
    playlist_features_list = ["artist", "album", "track_name", "track_id", "danceability", "energy", "key", "loudness",
                              "mode", "speechiness", "instrumentalness", "liveness", "valence", "tempo", "duration_ms",
                              "time_signature"]

    playlist_df = pd.DataFrame(columns=playlist_features_list)

    # Loop through every track in the playlist, extract features and append the features to the playlist df

    playlist = sp.user_playlist_tracks(creator, playlist_id)["items"]
    for track in playlist:
        
        playlist_features = {}
        
        #Fetch metadata
        playlist_features["artist"] = track["track"]["album"]["artists"][0]["name"]
        playlist_features["album"] = track["track"]["album"]["name"]
        playlist_features["track_name"] = track["track"]["name"]
        playlist_features["track_id"] = track["track"]["id"]

        #Fetch features
        audio_features = sp.audio_features(playlist_features["track_id"])[0]
        for feature in playlist_features_list[4:]:
            playlist_features[feature] = audio_features[feature]

        #Combine dataframes
        track_df = pd.DataFrame(playlist_features, index=[0])
        playlist_df = pd.concat([playlist_df, track_df], ignore_index=True)

    playlist_df.to_csv("filepath/filename")
    return playlist_df


df = analyze_playlist(username, playlist_id)


av_column = df.mean(axis=0)
print(av_column)

name = 'Johnny Cash'

artist_name = name
artist_name_clean = artist_name.replace(' ', '')
artist_name_clean = artist_name_clean.lower()
#current_path = os.getcwd()
csv_name = artist_name_clean + '_features' + '.csv'

df.to_csv(csv_name)
