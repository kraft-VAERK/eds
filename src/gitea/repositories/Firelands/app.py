try: 
    import requests
except:
    print("requests module not found, please install it by running 'pip install requests'")

def get_server_response():
    url = 'http://python-server:5000'
    response = requests.get(url)
    if response.status_code == 200:
        print("Connection successful!")
        print(f"Server response: {response.text}")
        return True
    else:
        print("Failed to connect to the server.")
        return False
print("Nice job on the step, start on the services next and you'll be cracking in no time!")
try:
    x = get_server_response()
    if x == True:
        print("Service seen, move on to the next step!")
    else:
        print("Service not seen, check the server and try again")    
except:
    print("service not found")