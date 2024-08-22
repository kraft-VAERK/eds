import requests
from base64 import b64encode


class DroneBase:
    BASE_URL = 'https://full-enormous-crow.ngrok-free.app'
    API_BASE_URL = f'{BASE_URL}/api/v1'
    token = None  
    
    def basic_auth(self, username, password):
        token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
        return f'Basic {token}'
    
    def create_header(self):
        header={
            'accept': 'application/json',
            'authorization': f"{self.token}",
            'Content-Type': 'application/json',
            'Host': 'full-enormous-crow.ngrok-free.app',
            'Cookie': 'abuse_interstitial=full-enormous-crow.ngrok-free.app;'
        }
        return header
    
    def post(self, endpoint, **kwargs):
        return requests.post(f'{self.API_BASE_URL}{endpoint}' , headers=self.create_header(), **kwargs)
    
    def get(self, endpoint, **kwargs):
        return requests.get(f'{self.API_BASE_URL}{endpoint}', headers=self.create_header(), **kwargs)
    
    def put(self, endpoint, **kwargs):
        return requests.put(f'{self.API_BASE_URL}{endpoint}', headers=self.create_header(), **kwargs)
    def delete(self, endpoint, **kwargs):
        return requests.delete(f'{self.API_BASE_URL}{endpoint}', headers=self.create_header(), **kwargs)