import requests
import base64
import datetime

class SpotifyApi(object):

	access_token = None
	access_token_expires = datetime.datetime.now()
	access_token_did_expire = True
	client_id = None
	client_secret = None
	token_url = "https://accounts.spotify.com/api/token"

	def __init__(self, client_id, client_secret, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.client_id = client_id
		self.client_secret = client_secret

	def get_client_credentials(self):
		"""
		Returns base 64 encoded string
		"""
		client_id = self.client_id
		client_secret = self.client_secret

		if client_id is None or client_secret is None:
			raise Exception(" You must set client_id and client_secret ")

		client_creds = f"{client_id}:{client_secret}"
		base64_encoded_client_creds = base64.b64encode(client_creds.encode())
		return base64_encoded_client_creds.decode()

	def get_token_header(self):

		base64_encoded_client_creds = self.get_client_credentials()
		return {
			"Authorization": f"Basic {base64_encoded_client_creds}"
		}

	def get_token_data(self):
		return {
			"grant_type": "client_credentials"
		}

	def perform_auth(self):

		token_url = self.token_url
		token_data = self.get_token_data()
		token_headers = self.get_token_header()
		r = requests.post(token_url, data = token_data, headers = token_headers)

		if r.status_code not in range(200,299):
			return False

		data = r.json()
		now = datetime.datetime.now()
		access_token = data['access_token']
		expires_in = data['expires_in']
		expires = now + datetime.timedelta(seconds=expires_in)

		self.access_token = access_token

		self.access_token_expires = expires
		self.access_token_did_expire = expires < now

		return True

client_id = ''
client_secret = ''


client = SpotifyApi(client_id, client_secret)
client.perform_auth()

print(client.access_token)

