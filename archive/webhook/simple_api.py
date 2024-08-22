from flask import Flask, request
import requests
from pprint import pprint
import os
from test_ssh import check_ssh_connection

machines = ["130.225.38.243"]


data = {
    "Machine-1:130.225.38.190": {
        "name": "CTF-Machine-1",
        "status": "online",
    },
    "Machine-2:130.225.38.227": {
        "name": "CTF-Machine-2",
        "status": "online",
    }
}
def test_connection(url, headers=None):
    try:
        r = requests.get(url, headers=headers)
        print(r.status_code, r.text)
        return r.status_code == 200
    except:
        return False
    
app = Flask(__name__)
@app.route('/', methods=['GET'])
def index():
    return 'OK'    
@app.route('/hook', methods=['POST', 'GET'])
def hook():
    data = request.get_json()
    headers = request.headers
    print(data['action'], headers.get('X-Gitea-Event') )
    if data['action'] == 'closed' or headers.get('X-Gitea-Event') == 'push':
        print("Pull request closed")
        return "Pull request closed", 200
    if headers.get('X-Gitea-Event') == 'pull_request':
        ref = data['pull_request']['base']['ref']
        commit = data['pull_request']['head']['sha']
        state = data['pull_request']['state']
        action = data['action']
    else:
        ref = data["ref"]
        commit = data["after"]
    repos = data["repository"]["full_name"]
    for i in range(0,3):
        connection_test = test_connection(f"http://localhost:808{i}/api/user", {"Authorization": f"Bearer {request.args.get('secret')}"})
        print(connection_test)
        if connection_test:
            print("Connection to DroneCI established")
            try:
                url = f"http://localhost:808{i}/api/repos/{repos}/builds?branch={ref.split('/')[-1]}"
                r = requests.post(url, headers={"Authorization": f"Bearer {request.args.get('secret')}"})
                if i == 0 and r.status_code == 200:
                    print(f"Posted to build, to port 808{i} aau-cluster-deployment machines")
                    return 'Build posted, return code from DroneCI:', r.status_code
                elif i == 1 and r.status_code == 200:
                    print(f"Posted to build to port 808{i}")
                    return 'Build posted, return code from DroneCI:', r.status_code
                elif i == 2 and r.status_code == 200:
                    print(f"Posted to build to port 808{i} CTF-machine-2")
                    return 'Build posted, return code from DroneCI:', r.status_code
            except:
                print("Failed to post to build")
                return 'Failed to post to build', 500
        else:
            continue
    return 'OK'



@app.route('/abberus_hook', methods=['POST', 'GET'])
def abberus_hook():
    data = request.get_json()
    headers = request.headers
    if data['action'] == 'closed' or headers.get('X-Gitea-Event') == 'push':
        print("Pull request closed")
        return "Pull request closed", 200
    if headers.get('X-Gitea-Event') == 'pull_request':
        ref = data['pull_request']['base']['ref']
        commit = data['pull_request']['head']['sha']
        state = data['pull_request']['state']
        action = data['action']
    else:
        ref = data["ref"]
        commit = data["after"]
    repos = data["repository"]["full_name"]
    for i in range(0,3):
        connection_test = test_connection(f"http://localhost:808{i}/api/user", {"Authorization": f"Bearer {request.args.get('secret')}"})
        if connection_test:
            print("Connection to DroneCI established")
            try:
                url = f"http://localhost:808{i}/api/repos/{repos}/builds?branch={ref.split('/')[-1]}"
                r = requests.post(url, headers={"Authorization": f"Bearer {request.args.get('secret')}"})
                if i == 0 and r.status_code == 200:
                    print(f"Posted to build, to port 808{i} aau-cluster-deployment machines")
                    return 'Build posted, return code from DroneCI:', r.status_code
                elif i == 1 and r.status_code == 200:
                    print(f"Posted to build to port 808{i}")
                    return 'Build posted, return code from DroneCI:', r.status_code
                elif i == 2 and r.status_code == 200:
                    print(f"Posted to build to port 808{i} CTF-machine-2")
                    return 'Build posted, return code from DroneCI:', r.status_code
            except:
                print("Failed to post to build")
                return 'Failed to post to build', 500
        else:
            continue
    return 'OK'


@app.route('/amirdrassil_hook', methods=['POST', 'GET'])
def amirdrassil_hook():
    data = request.get_json()
    headers = request.headers
    for i in range(0,3):
        ref = data["ref"]
        repos = data["repository"]["full_name"]
        connection_test = test_connection(f"http://localhost:808{i}/api/user", {"Authorization": f"Bearer {request.args.get('secret')}"} )
        if connection_test:
            try:
                url = f"http://localhost:808{i}/api/repos/{repos}/builds?branch={ref.split('/')[-1]}"
                r = requests.post(url, headers={"Authorization": f"Bearer {request.args.get('secret')}"})
                if i == 0 and r.status_code == 200:
                    print(f"Posted to build, to port 808{i} aau-cluster-deployment machines")
                    return 'Build posted, return code from DroneCI:', r.status_code
                elif i == 1 and r.status_code == 200:
                    print(f"Posted to build to port 808{i}")
                    return 'Build posted, return code from DroneCI:', r.status_code
                elif i == 2 and r.status_code == 200:
                    print(f"Posted to build to port 808{i} CTF-machine-2")
                    return 'Build posted, return code from DroneCI:', r.status_code
            except:
                print('Failed to post to build', 500)
    return 'Fail', 500

app.route("/ulduar_hook", methods=['POST', 'GET'])
def ulduar_hook():
    data = request.get_json()
    headers = request.headers
    for i in range(len(machines)):
        print("hello")
    return 'Fail'



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
