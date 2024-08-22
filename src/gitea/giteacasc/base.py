import requests
from base64 import b64encode


class GiteaBase:
    BASE_URL = 'https://git.devops.hkn'
    API_BASE_URL = f'{BASE_URL}/api/v1'
    token = None

    def post(self, endpoint, **kwargs):
        return requests.post(f'{self.API_BASE_URL}{endpoint}',
                             headers={'Authorization': f'token {self.token}'}, verify=False, **kwargs)

    def get(self, endpoint, **kwargs):
        return requests.get(f'{self.API_BASE_URL}{endpoint}',
                            headers={'Authorization': f'token {self.token}'}, verify=False, **kwargs)

    def put(self, endpoint, **kwargs):
        return requests.put(f'{self.API_BASE_URL}{endpoint}',
                            headers={'Authorization': f'token {self.token}'}, verify=False, **kwargs)
    
    def basic_auth(self, username, password):
        token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
        return f'Basic {token}'
    
    def create_header(self, username, password):
        header={
            'accept': 'application/json',
            'authorization': f"{self.basic_auth(username, password)}",
            'Content-Type': 'application/json'
        }
        return header
