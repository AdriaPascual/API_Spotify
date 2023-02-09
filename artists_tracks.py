from auth import Auth
import requests
import csv 

class SpotifyAPI:

    def __init__(self):
        self.base_url = 'https://api.spotify.com/v1/'
        self.auth = Auth()
        self.token = self.auth.get_token()
        self.list_artists = []
        self.artists_for_tracks = {}
        self.genres_count = {}
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            "Content-Type": "application/json"
        }
        self.params = {
            'limit': 10,
            'time_range': 'long_term'
        }

    def status_code(self):
        self.response_artist = requests.get(self.base_url+'me/top/artists',params =self.params, headers=self.headers)
        self.response_tracks = requests.get(self.base_url+'me/top/tracks',params=self.params, headers=self.headers)        
        if self.response_artist.status_code != 200:
            raise Exception(f"Error obteniendo los detalles del usuario: {self.response_artist.json()['error']['message']}")
        if self.response_tracks.status_code != 200:
            raise Exception(f"Error obteniendo los detalles del usuario: {self.response_tracks.json()['error']['message']}")        

    def artist_user(self):
        self.response = requests.get(self.base_url+'me/top/artists',params =self.params, headers=self.headers)
        self.data = self.response.json()
        for artist in self.data["items"]:
            self.list_artists.append(artist)
        with open('output_files/artists_genres.csv', 'a') as artistas_y_generos:
            fieldnames = ['artist', 'genre']
            writer = csv.DictWriter(artistas_y_generos, fieldnames=fieldnames)
            writer.writeheader()
            for artist in self.list_artists:
                if 'genres' in artist:
                    for genre in artist["genres"]:
                        if genre in self.genres_count.keys():
                            self.genres_count[genre] += 1
                        else:
                            self.genres_count[genre] = 1
                        writer.writerow({'artist': artist['name'], 'genre': genre})
        print("La información de los diez artistas más escuchados y sus géneros ha sido guardada con éxito")


    def tracks_user(self):
        self.response = requests.get(self.base_url+'me/top/tracks',params=self.params, headers=self.headers)
        self.data = self.response.json()
        with open('output_files/tracks_artists.csv', 'a') as canciones_y_artistas:
            fieldnames = ['track', 'artist']
            writer = csv.DictWriter(canciones_y_artistas, fieldnames=fieldnames)
            writer.writeheader()
            for track in self.data["items"]:
                artist = track["artists"][0]["name"]
                if artist in self.artists_for_tracks.keys():
                    self.artists_for_tracks[artist].append(track["name"])
                else: 
                    self.artists_for_tracks[artist] = [track["name"]]
                writer.writerow({'track': track["name"], 'artist': artist})
        print("La información de las diez canciones más escuchadas y su artista ha sido guardada con éxito")