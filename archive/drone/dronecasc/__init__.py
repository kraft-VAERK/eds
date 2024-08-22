from pprint import pprint
import click
import yaml
from dronecasc.drone import Drone
import os
import logging
import http.client
from faker import Faker
from slugify import slugify

# http.client.HTTPConnection.debuglevel = 1
# logging.basicConfig(level=logging.DEBUG)

@click.command()
@click.argument('path', type=str)
@click.option('-u', '--username', 'username', help='Username.')
@click.option('-p', '--password', 'password', help='Password.')
@click.option('-s', '--secret', 'secret', help='Pass secret from Drone')
def dronecasc(path, username=None, password=None, secret=None):
    fake = Faker(debuglevel=0)
    with open(path, 'r') as y:
        config = yaml.safe_load(y.read())
    project_dir = os.path.dirname(os.path.abspath(__file__))
    admin_username = "morten_jakobsen"
    admin_password = "escrow"
    if secret == None:
        company_name = fake.company()
        company_name = slugify(company_name)
        first_org_name = next(iter(config['orgs']))
        config['orgs'][company_name] = config['orgs'].pop(first_org_name)
        with open(path, 'w') as y:
            yaml.dump(config, y)
    g = Drone(admin_username, admin_password)
    # If statement is so that the module can be called with two desired goals.
    # "Creation Phase"
    # If there is no secret passed, the module is still in "creation phase", meaning that it will create the users, organizations, and repos.
    # If there is a secret passed, the module is in "hook phase", meaning that it will create the webhooks for the repos.
    if secret == None:
        if password is not None and username is not None:
            os.environ['GIT_ASKPASS'] = os.path.join(project_dir, 'askpass.py')
            os.environ['GIT_USERNAME'] = username
            os.environ['GIT_PASSWORD'] = password
            # Add the new username as a collaborator with write permission
            user = g.create_user(username, fake.email(), password,  False, redirect_url="http://localhost:8080/login")
            if user.status_code != 201:
                print(int(1))
                return "Error creating user."
        else:
            username = fake.user_name()
            password = fake.password()
            user = g.create_user(username, fake.email(), password, False, redirect_url="http://localhost:8080/login")
            if user.status_code != 201:
                print(int(1))
                return "Error creating user."
        # From drone.yaml file, create the organizations and add the user to the maintainer group.
        if Drone.YAML_ORGS in config:
            for org_name in config[Drone.YAML_ORGS]:
                # Create the organization, create repos.
                config['orgs'][org_name]['teams']['Maintainers']['members'].append(username)
                config['orgs'][org_name]['repos']['Abberus']['collaborators'][username] = 'write'
                config['orgs'][org_name]['repos']['Amirdrassil']['collaborators'][username] = 'write'
                config['orgs'][org_name]['repos']['Ulduar']['collaborators'][username] = 'read'
                config['orgs'][org_name]['repos']['Icecrown']['collaborators'][username] = 'write'
                org = g.create_org(admin_username, org_name, **config[Drone.YAML_ORGS][org_name])
                if org.status_code != 201:
                    print(int(1))
                    return "Error creating organization."
        print(int(0))
        return "Success."
    # "Hook Phase"
    # Because this is needed is because the secret from the local instance of drone is needed to create the webhooks.
    # Otherwise the authorization headers will not be correct, and drone with return a 401.
    if secret != None:
        for x in config['orgs']:
            y = config['orgs'][x]['repos']
            for z in y:
                if z == "Abberus":
                    abberus_url = f"http://130.225.38.239:5000/abberus_hook?secret={secret}"
                    abbers_url_2 = f"http://130.225.38.239:8080/abberus_hook?secret=super-duper"
                    abberus_w1 = g.create_webhook_abberus(abberus_url, x, z)
                    abberus_w2 = g.create_webhook_abberus(abbers_url_2, x, z)
                    if 201 not in [abberus_w1.status_code, abberus_w2.status_code]:
                        print(1)
                        return "Error creating webhooks."
                if z == "Amirdrassil":
                    amirdrassil_url = f"http://130.225.38.239:5000/amirdrassil_hook?secret={secret}"
                    amirdrassil_w1 = g.create_webhook_amirdrassil(amirdrassil_url, x, z)
                    if 201 not in [amirdrassil_w1.status_code]:
                        print(1)
                        return "Error creating webhooks."                    
        print(0)
        return "Success."
    