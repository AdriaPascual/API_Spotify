from auth import Auth
import urllib.request
import requests

class Playlist:
    def __init__(self) -> None:
        self.base_url = 'https://api.spotify.com/v1/'
        self.playlist_id = '37i9dQZF1DWWGFQLoP9qlv'
        self.auth = Auth()
        self.token = self.auth.get_token()

        self.headers = {
            'Authorization': f'Bearer {self.token}',
            "Content-Type": "application/json"
        }

    def status_code(self):
        self.response = requests.get(self.base_url + 'playlists/' + self.playlist_id, headers= self.headers)
        if self.response.status_code != 200:
            raise Exception(f"Error obteniendo los detalles de la lista de reproducción: {self.response.json()['error']['message']}")
              
    
    def cover_playlist(self):
        self.response = requests.get(self.base_url + 'playlists/' + self.playlist_id, headers= self.headers)
        self.data = self.response.json()

        if "images" in self.data:
            __cover_url = self.data["images"][0]["url"]
            urllib.request.urlretrieve(__cover_url, 'output_files/image_cover.jpg')
            print("La imagen de la portada ha sido guardada con éxito")
        else:
            print("La playlist no tiene imagen asociada")
        


    def get_followers(self):
        self.data = self.response.json()
        __followers = self.data["followers"]["total"]
        with open('output_files/followers.csv', 'a') as f:
            f.write(str(__followers) + '\n')
        print("La información de los seguidores ha sido guardada con éxito")

   

    def average_track_attributes(self):
        self.response = requests.get(self.base_url + 'playlists/' + self.playlist_id, headers= self.headers)
        self.data = self.response.json()
        total_tracks = len(self.data["tracks"]['items'])
        
        tempo_sum = 0
        acousticness_sum = 0
        danceability_sum = 0
        energy_sum = 0
        instrumentalness_sum = 0
        liveness_sum = 0
        loudness_sum = 0
        valence_sum = 0

        for track in self.data["tracks"]["items"]:
            track_response = requests.get(track["track"]['href'], headers= self.headers)
            if track_response.status_code != 200:
                raise Exception(f"Error obteniendo los detalles de la canción: {track_response.json()['error']['message']}")
            track_data = track_response.json()
            track_id = track_data["id"]
            track_features = requests.get(f'{self.base_url}audio-features/{track_id}', headers=self.headers).json()
            
            tempo_sum += track_features["tempo"]
            acousticness_sum += track_features["acousticness"]
            danceability_sum += track_features["danceability"]
            energy_sum += track_features["energy"]
            instrumentalness_sum += track_features["instrumentalness"]
            liveness_sum += track_features["liveness"]
            loudness_sum += track_features["loudness"]
            valence_sum += track_features["valence"]

        tempo_avg = tempo_sum / total_tracks
        acousticness_avg = acousticness_sum / total_tracks
        danceability_avg = danceability_sum / total_tracks
        energy_avg = energy_sum / total_tracks
        instrumentalness_avg = instrumentalness_sum / total_tracks
        liveness_avg = liveness_sum / total_tracks
        loudness_avg = loudness_sum / total_tracks
        valence_avg = valence_sum / total_tracks

        with open('output_files/average_track_attributes.csv', 'w') as f:
            f.write('tempo,acousticness,danceability,energy,instrumentalness,liveness,loudness,valence\n')
            f.write(f"{tempo_avg},{acousticness_avg},{danceability_avg},{energy_avg},{instrumentalness_avg},{liveness_avg},{loudness_avg},{valence_avg}\n")
        print("La información de las características promedio de las canciones ha sido guardada con éxito")

        
