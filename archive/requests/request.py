import requests
import base64
import sys

def oauth_request(username, password):
    base64_credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
    # The Redirect URL might change depending the amount of user, but first prove
    # 1-1 and the n-1 meaning that i want to prove first 1 user to 1 gitea instance and then n users to 1 gitea instance
    data = {
        "name": f'{username}-oauth',
        "redirect_uris": ["http://localhost:8080/login"]
    }
    # Headers for the request,
    # Only one worth mentioning is Cookie. Since the gitea instance is behind ngrok, we need to set the cookie to the ngrok domain
    # This is done by setting the Cookie header to "abuse_interstitial=full-enormous-crow.ngrok-free.app;" 
    headers = {
        "content-Type": "application/json",
        "accept": "application/json",
        "authorization": f"Basic {base64_credentials}",
        "cookie": "abuse_interstitial=full-enormous-crow.ngrok-free.app;"
    }
    endpoint = 'https://full-enormous-crow.ngrok-free.app/api/v1/user/applications/oauth2'
    
    res = requests.post(endpoint, headers=headers, json=data)

    if res.status_code != 201:
        print("Error")
    else:
        return res.json()

if __name__ == "__main__":
    # Check if the correct number of command line arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python script.py <Username> <Password>")
        sys.exit(1)

    # Get the command line arguments
    username = sys.argv[1]
    password = sys.argv[2]

    # Make the OAuth request
    result = oauth_request(username, password)

    print(result)