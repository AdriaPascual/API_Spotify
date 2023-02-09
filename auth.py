import requests
import base64
import json
import datetime
import webbrowser
import binascii
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

state = binascii.hexlify(os.urandom(20)).decode('utf-8')
code = None

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global code
        self.close_connection = True
        query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        if not query['state'] or query['state'][0] != state:
            raise RuntimeError("state argument missing or invalid")
        code = query['code']

class Auth:

    __client_id = '19dc7240ad15470694e73f4fe8edd854'
    __client_secret = 'd3c96edd61c3414eab2f2653d322d75a'
    __server = 'localhost'
    __port = 8080
    __redirect_uri = f'http://{__server}:{__port}'
    __base_url = 'https://accounts.spotify.com/'
    __auth_endpoint = 'authorize'
    __get_token_endpoint = 'api/token'
    __auth_file = 'f_token.json'
    __scope = ['user-top-read','user-read-email']

    def __init__(self):
        self.__data = None

    def generate_token(self):
        url = self.__create_oauth_link()
        webbrowser.open_new_tab(url)

        server = HTTPServer((Auth.__server, Auth.__port), RequestHandler)
        server.handle_request()

        token, refresh_token, expires_in = self.__exchange_code_for_access_token(code)
        self.__save_token_to_file(token, refresh_token, expires_in)

    def get_token(self):
        self.__load_token_from_file()
        now = datetime.datetime.now()
        if now > datetime.datetime.fromisoformat(self.__data['expires']):
            self.__refresh_token()
        else:
            return self.__data['token']

    def __create_oauth_link(self):

        params = {
            "client_id": Auth.__client_id,
            "redirect_uri": Auth.__redirect_uri,
            "response_type": "code",
            "scope" : ' '.join(Auth.__scope),
            "state" : state
        }

        endpoint = Auth.__base_url + Auth.__auth_endpoint
        response = requests.get(endpoint, params=params)

        if response:
            url = response.url
            return url
        else:
            raise Exception("Could Not Get An Url...")

    def __exchange_code_for_access_token(self, code=None):
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": Auth.__redirect_uri,
        }

        auth_header = base64.b64encode(f'{Auth.__client_id}:{Auth.__client_secret}'.encode())

        headers = {"Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {auth_header.decode('ascii')}"}

        endpoint = Auth.__base_url + Auth.__get_token_endpoint

        response = requests.post(endpoint, data=data, headers=headers)
        response_json = response.json()

        if response:
            return response_json["access_token"], response_json["refresh_token"], response_json['expires_in']
        else:
            raise Exception("Could Not Get Token...")

    def __save_token_to_file(self, token, refresh_token, expires_in):
        expires = datetime.datetime.now() + datetime.timedelta(seconds = expires_in)
        with open(Auth.__auth_file, 'w') as file:
            json.dump({"token":token, "refresh_token":refresh_token, "expires": expires.isoformat()}, file)

    def __load_token_from_file(self):
        with open(Auth.__auth_file, 'r') as file:
            self.__data = json.load(file)

    def __refresh_token(self):
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.__data['refresh_token']
        }

        auth_header = base64.b64encode(f'{Auth.__client_id}:{Auth.__client_secret}'.encode())

        headers = {"Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {auth_header.decode('ascii')}"}

        endpoint = Auth.__base_url + Auth.__get_token_endpoint

        response = requests.post(endpoint, data=data, headers=headers)
        response_json = response.json()

        if response:
            return response_json["access_token"], response_json["refresh_token"], response_json['expires_in']
        else:
            raise Exception("Could Not Get Token...")

            