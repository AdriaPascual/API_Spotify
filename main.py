from artists_tracks import SpotifyAPI
from auth import Auth
from playlist import Playlist

auth = Auth()
auth.generate_token()    # use it only for the first time
token = auth.get_token()

user_request = SpotifyAPI()
user_request.status_code()
user_request.artist_user()
user_request.tracks_user()

playlist_request = Playlist()
playlist_request.status_code()
playlist_request.cover_playlist()
playlist_request.get_followers()
playlist_request.average_track_attributes()



