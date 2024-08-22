import requests
import sys
from pprint import pprint

import yaml


def restore_data():
    data = {
    'orgs': {
        'value_1': {
            'teams': {
                'Maintainers': {
                    'permission': 'write',
                    'members': ['harambe', 'jacopo', 'marco']
                }
            },
            'repos': {
                'Abberus': {
                    'private': False,
                    'code': 'repositories/Abberus',
                    'collaborators': {
                        'harambe': 'write',
                        'marco': 'read',
                        'jacopo': 'administrator'
                    },
                    'branch_protections': {
                        'main': {
                            'required_approvals': 2
                        }
                    }
                }
            }
        }
    }
}
    with open('drone.yaml', 'w') as y:
        yaml.dump(data, y)
    return 0

data =  {
  "config_path": ".drone.yml",
  "protected": False,
  "trusted": False,
  "timeout": 60,
  "visibility": "internal"
}


# Check if the correct number of arguments is provided
if len(sys.argv) != 2:
    print("Usage: python script.py <credentials>")
    sys.exit(1)
# x = "morten_jakobsen:escrow"
with open('drone.yaml', 'r') as y:
    config = yaml.safe_load(y.read())
credentials = sys.argv[1]
# Extract arguments
for x in config['orgs']:
    # print(config['orgs'][x]['repos'])
    for i in config['orgs'][x]['repos']:
        url = f"http://localhost:8080/api/repos/{x}/{i}"
        print(url)
        print(i)
        if i == "Abberus":
            print("In Abberus")
            # Activating the repository on drone. This has to done by the owner of the repository on Gitea
            response = requests.post(url, headers={"Authorization": f"Bearer {credentials}"})            
            # Create secret number 1
            secret_1 = {    "name": "docker_username",  "data": "stiefbruder",  "pull_request": True    }
            # Secret number 2
            secret_2 = {    "name": "docker_password",  "data": "EDS{I_am_a_secret_password_1234}", "pull_request": True    }
            # Store secret in a list for iteration into Drone
            secrets = [secret_1, secret_2]
            r_l = requests.get(url + f"/secrets", headers={"Authorization": f"Bearer {credentials}"})
            # Repository Secret
            r_q = requests.patch(url=url, headers={"Authorization": f"Bearer {credentials}"}, json=data)
            for secret in secrets:
                response = requests.post(url + f"/secrets", headers={"Authorization": f"Bearer {credentials}"}, json=secret)
        if i == "Amirdrassil":
            print("In Amirdrassil")
            response = requests.post(url, headers={"Authorization": f"Bearer {credentials}"})
            secret_1 = {    "name": "mysql-username", "data": "photoview", "pull_request": False }
            secret_2 = {    "name": "mysql-password", "data": "password123", "pull_request": False}
            secret_3 = {    "name": "postgres-username", "data": "photoview_pg", "pull_request": False}
            secret_4 = {    "name": "postgres-password", "data": "photoview_pg_password", "pull_request": False}
            secrets = [secret_1, secret_2, secret_3, secret_4]
            for secret in secrets:
                response = requests.post(url + f"/secrets", headers={"Authorization": f"Bearer {credentials}"}, json=secret)
                print(response.status_code)
        if i == "Ulduar":
            print("In Ulduar")
            response = requests.post(url, headers={"Authorization": f"Bearer {credentials}"})
            
        if i == "Icecrown":
            print("In Icecrown")
            response = requests.post(url, headers={"Authorization": f"Bearer {credentials}"})