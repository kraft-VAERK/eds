from pprint import pprint
from binascii import hexlify
from hashlib import pbkdf2_hmac
from time import time,sleep
import requests
from dronecasc.base import DroneBase
from requests.auth import HTTPBasicAuth
import json
import git
import random
import string

class Drone(DroneBase):
    YAML_USERS = 'users'
    YAML_ORGS = 'orgs'
    YAML_REPOS = 'repos'
    
    def __init__(self, username, password):
        try:
            res = requests.post(f'{self.API_BASE_URL}/users/{username}/tokens',
                                auth=HTTPBasicAuth(username, password),
                                json={'name': f"token{''.join(random.choices(string.ascii_lowercase, k=23))}"})
            DroneBase.token = f"token {res.json()['sha1']}"
        except KeyError:
            res.raise_for_status()
    def get_users(self):
        res = self.get('/admin/users')
        if res.status_code in [200, 201]:
            res.raise_for_status()
        try:
            json_response = res.json()
            formatted_response = json.dumps(json_response, indent=2)
        except json.JSONDecodeError:
            return res.text
        return formatted_response
    
    def create_user(self, username, email, password, must_change_password=False, token=None, redirect_url=None):
        data = { "username": username, "email": email, "password": password, "must_change_password": must_change_password}
        res = self.post('/admin/users', json=data)
        if res.status_code != 201:
            res.raise_for_status()
        # user = User(res.json()['id'], username, email, must_change_password)
        return res    

    def create_org(self, owner_name, org_name, teams=None, repos=None):
        res = self.get(f'/admin/orgs')
        if res.status_code != 200:
            res.raise_for_status()
        for org in res.json():
            if org_name == org['username']:
                return Org(org_name)
        res = self.post(f'/admin/users/{owner_name}/orgs', json={'username': org_name})
        if res.status_code != 201:
            res.raise_for_status()
        org = Org(org_name)
        if teams:
            for team in teams:
                org.create_team(team, **teams[team])
        if repos:
            for name in repos:
                org.create_repo(name, **repos[name])
        return res
    def create_webhook_abberus(self, url, org, repo):
        res = self.post(f'/repos/{org}/{repo}/hooks',
                        json={'active': True,
                              'type': 'gitea',
                              'config': {'url': url, 'content_type': 'json'},
                              'events': ['pull_request'],
                              'branch_filter': 'main'
                              })
        return res
    def create_webhook_amirdrassil(self, url, org, repo):
        res = self.post(f'/repos/{org}/{repo}/hooks',
                        json={'active': True,
                              'type': 'gitea',
                              'config': {'url': url, 'content_type': 'json'},
                              'events': ['push'],
                              'branch_filter': 'main'
                              })
        return res

class Org(DroneBase):
    UNITS = ["repo.code",
             "repo.issues",
             "repo.ext_issues",
             "repo.wiki",
             "repo.pulls",
             "repo.releases",
             "repo.projects",
             "repo.ext_wiki"]

    def __init__(self, org_name):
        self.name = org_name

    def create_team(self, name, permission, members):
        res = self.post(f'/orgs/{self.name}/teams',
                        json={'name': name,
                              'permission': permission,
                              'units': self.UNITS})
        if res.status_code != 201:
            res.raise_for_status()
        for username in members:
            res_create_team_member = self.put(f"/teams/{res.json()['id']}/members/{username}")
            if res_create_team_member.status_code != 204:
                res.raise_for_status()

    def create_repo(self, name, private, code=None, default_branch='main', collaborators=None,
                    branch_protections=None, teams=None, releases=None, webhooks=None):
        res = self.post(f'/orgs/{self.name}/repos', json={'name': name,
                                                          'default_branch': default_branch,
                                                          'private': private})
        if res.status_code != 201:
            res.raise_for_status()
        repo = Repo(self.name, name, private, default_branch)
        if code:
            repo.push_code(code)
        if collaborators:
            for collaborator in collaborators:
                repo.add_collaborator(collaborator, collaborators[collaborator])
        if branch_protections:
            for branch in branch_protections:
                repo.set_branch_protection(branch, **branch_protections[branch])
        if teams:
            for name in teams:
                repo.add_team(name)
        if releases:
            for name in releases:
                repo.create_release(name, **releases[name])
        if webhooks:
            for url in webhooks:
                repo.create_webhook(url, **webhooks[url])
        return repo


class Repo(DroneBase):
    def __init__(self, org_name, repo_name, private, default_branch):
        self.org = org_name
        self.name = repo_name
        self.private = private
        self.default_branch = default_branch

    def push_code(self, git_repo_path):
        try:
            repo = git.Repo(git_repo_path)
            repo.git.push(f'https://morten_jakobsen:escrow@full-enormous-crow.ngrok-free.app/{self.org}/{self.name}.git', '--tags', '-u', self.default_branch)
        except git.exc.GitCommandError as e:
            print(e)
            print('make sure remote origin points to "localhost:3000" and the default branch is "main"')
            exit()

    def add_collaborator(self, collaborator, permission):
        res = self.put(f'/repos/{self.org}/{self.name}/collaborators/{collaborator}',
                       json={'permission': permission})
        if res.status_code != 204:
            res.raise_for_status()

    def set_branch_protection(self, branch, **kwargs):
        res = self.post(f'/repos/{self.org}/{self.name}/branch_protections',
                        json={'branch_name': branch, **kwargs})
        if res.status_code != 201:
            res.raise_for_status()

    def add_team(self, name):
        res = self.put(f'/repos/{self.org}/{self.name}/teams/{name}')
        if res.status_code != 204:
            res.raise_for_status()

    def create_release(self, name, **kwargs):
        sleep(0.5)
        res = self.post(f'/repos/{self.org}/{self.name}/releases', json={'name': str(name), **kwargs})
        if res.status_code != 201:
            print('error:', name, kwargs, res.text)
            res.raise_for_status()

    def create_webhook(self, url, **kwargs):
        res = self.post(f'/repos/{self.org}/{self.name}/hooks',
                        json={'active': True,
                              'type': 'gitea',
                              'config': {'url': url, 'content_type': 'json'},
                              'events': ['pull_request'],
                              'branch_filter': 'main'
                              **kwargs})
        if res.status_code != 201:
            res.raise_for_status()