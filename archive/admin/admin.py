import requests
from requests.auth import HTTPBasicAuth

class Admin():
    OWNER = "morten_jakobsen"
    PASSWORD ="escrow"
    GITEA_URL = "git.devops.eds"
    ACCESS_TOKEN = ""
    headers = {
    "Authorization" : f"{ACCESS_TOKEN}"
    }
    
    def __init__(self):
        res = requests.get(f"{self.GITEA_URL}/users/{self.OWNER}/tokens", 
                            auth=HTTPBasicAuth(self.OWNER, self.PASSWORD))
        if res != 200:
            res.raise_for_status()
        names_list = [item['name'] for item in res.json()]
        if "admin_token" in names_list:
            requests.delete(f"{self.GITEA_URL}/users/{self.OWNER}/tokens/admin_token",auth=HTTPBasicAuth(self.OWNER, self.PASSWORD))
            res = requests.post(f'{self.GITEA_URL}/users/{self.OWNER}/tokens',
                            auth=HTTPBasicAuth(self.OWNER, self.PASSWORD),
                            json={'name': f"admin_token"})
            self.ACCESS_TOKEN = f"token {res.json()['sha1']}"
            self.headers['Authorization'] = f"token {res.json()['sha1']}"
            print("Token already exists")
            return None # Token already exists
        else:
            print("Creating token")
            res = requests.post(f'{self.GITEA_URL}/users/{self.OWNER}/tokens',
                            auth=HTTPBasicAuth(self.OWNER, self.PASSWORD),
                            json={'name': f"admin_token"})
            self.ACCESS_TOKEN = f"token {res.json()['sha1']}"
            self.headers['Authorization'] = f"token {res.json()['sha1']}"
            return None
    def get_tokens(self):
        res = requests.get(f"{self.GITEA_URL}/users/{self.OWNER}/tokens", 
                           auth=HTTPBasicAuth(self.OWNER, self.PASSWORD))
        if res != 200:
            res.raise_for_status()
        names_list = [item['name'] for item in res.json()]
        return names_list    
    def get_user_by_username(self, username):
        """
        Get a user by username.
        
        Args:
        - username (str): The username of the user to be retrieved.
        
        Returns:
        - dict: The API response as a dictionary.
        
        """
        response = requests.get(f"{self.GITEA_URL}/users/{username}", headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            return "Didnt find user."
    def get_users_repos(self, username):
        """
        Get the list of repositories owned by a user.
        
        Args:
        - username (str): The username of the user whose repositories are to be retrieved.
        
        Returns:
        - list: The API response as a list of dictionaries.
        
        """
        response = requests.get(f"{self.GITEA_URL}/repos/search", headers=self.headers)
        if response.status_code == 200:
            res = response.json()["data"]
            list_of_repos = [repo for repo in res if repo.get('owner', {}).get('username') == username]
            return list_of_repos
        else:
            return "Didnt find user."
    def change_repository_owner(self, repo_owner, repo_name, new_owner):
        """
        !! Does Not Work !!
        
        Change the repository owner from one user to another in Gitea.

        Args:
        - repo_owner (str): The current owner of the repository.
        - repo_name (str): The name of the repository.
        - new_owner (str): The username of the new owner.

        Returns:
        - dict: The API response as a dictionary.
        """
        transfer_url = f"https://full-enormous-crow.ngrok-free.app/{repo_owner}/{repo_name}/settings"
        transfer_data = {
            "action": "transfer",
            "repo_name": repo_name,
            "new_owner_name": new_owner
            }
        transfer_response = requests.post(transfer_url, json=transfer_data, headers=self.headers)
        print(transfer_response.status_code)
        print(transfer_response.text)        
        if transfer_response.status_code == 200:
            return {"success": f"Repository '{repo_name}' ownership transferred to '{new_owner}' successfully."}
        else:
            return {"error": f"Failed to transfer repository ownership. Status code: {transfer_response.status_code}"}
    def delete_repository(self, repo_owner, repo_name):
        """
        Deletes a repository on Gitea.

        Parameters:
        - repo_owner (str): The username of the repository owner.
        - repo_name (str): The name of the repository to be deleted.

        Returns:
        - str: A message indicating the result of the repository deletion.

        Note:
        - Ensure that the user associated with the provided API token has the necessary permissions
        to delete the repository.
        - This method makes a DELETE request to the Gitea API endpoint for repository deletion.
        - If the repository is successfully deleted, it returns a confirmation message.
        - If there is an error, it returns an error message along with the HTTP status code and response text.
        """
        try:
            response = requests.delete(f"{self.GITEA_URL}/repos/{repo_owner}/{repo_name}", headers=self.headers)
        except:
            return response
        return response
    def get_all_users(self):
        """
        Retrieves a list of all users from the Gitea instance.
        Returns:
        - list: A sorted list of user dictionaries containing user information.
                Each user dictionary includes attributes such as 'id', 'username', 'full_name', etc.
        Note:
        - This method makes a GET request to the Gitea API endpoint for retrieving all users.
        - If the request is successful (HTTP status code 200), it returns a sorted list of user dictionaries.
        - The list is sorted based on the 'id' attribute of each user.
        - Each user dictionary contains various attributes, such as 'id', 'username', 'full_name', etc.
        - If there is an error, it returns 0.
        """
        response = requests.get(f"{self.GITEA_URL}/admin/users", headers=self.headers)
        if response.status_code == 200:
            return sorted(response.json(), key=lambda x: x['id'])
        else:
            return response.raise_for_status()
    def delete_all(self):
        """
        Nuke method, deletes all users except the first 6.
        First 6 is used for the internal Gitea system and for the CTF's
        
        Args:
        - None
        
        Returns:
        - str: A string indicating the result of the deletion.
        
        Cauntion:
        Please dont use it.       
        """
        res = self.get_all_users()
        if type(res) == list:
            for user in res:
                if user["id"] >= 7:
                    print("Deleting user: " + user["username"])
                    res = self.delete_user(user["username"])
                    if res.status_code != 204:
                        return f"Error deleting user, {res.status_code}\n{res.text}"
                    else:
                        print(f"User {user['username']} deleted.")
            return "All users deleted."          
    def delete_user(self, username):
        user = self.get_user_by_username(username)
        repos = self.get_users_repos(username)
        if user != "Didnt find user.":
            if len(repos) > 0:
                for repo in repos:
                    if repo['owner']['username'] == user['username']:
                        print(f"Deletion of repository: {repo['name']} with owner {repo['owner']['username']}")
                        res = self.delete_repository(repo['owner']['username'], repo['name'])
            res = requests.delete(f"{self.GITEA_URL}/admin/users/{username}", headers=self.headers)
            return res
    def delete_team(self, team_id):
        """
        Deletes a team on Gitea.

        Parameters:
        - team_id (int): The ID of the team to be deleted.

        Returns:
        - str: A message indicating the result of the team deletion.

        Note:
        - This method makes a DELETE request to the Gitea API endpoint for team deletion.
        - If the team is successfully deleted, it returns a confirmation message.
        - If there is an error, it returns an error message along with the HTTP status code and response text.
        """
        response = requests.delete(f"{self.GITEA_URL}/teams/{team_id}", headers=self.headers)
        return response
    def delete_all_orgs(self):
        """
        Deletes an organization on Gitea.

        Parameters:
        - org_name (str): The name of the organization to be deleted.

        Returns:
        - str: A message indicating the result of the organization deletion.

        Note:
        - This method makes a DELETE request to the Gitea API endpoint for organization deletion.
        - If the organization is successfully deleted, it returns a confirmation message.
        - If there is an error, it returns an error message along with the HTTP status code and response text.
        """
        # org = requests.get(f"{self.GITEA_URL}/user/repos", headers=self.headers)
        orgs = requests.get(f"{self.GITEA_URL}/users/morten_jakobsen/orgs", headers=self.headers)
        # print(orgs.json()[0]['username'])
        # try:
        #     org_name = org.json()[0]['owner']['username']
        # except IndexError:
        #     return "No orgs to delete."
        for i in orgs.json():
            org_repos = requests.get(f"{self.GITEA_URL}/orgs/{i['username']}/repos", headers=self.headers)
            if len(org_repos.json()) > 0:
                for repo in org_repos.json():
                    print(f"Deletion of repository: {repo['name']} with owner {repo['owner']['username']}")
                    res = self.delete_repository(repo['owner']['username'], repo['name'])
                    if res.status_code != 204:
                        return res.raise_for_status()
                    else:
                        print(f"Correctly deleted org: {repo['name']}")
            response = requests.delete(f"{self.GITEA_URL}/orgs/{i['username']}", headers=self.headers)
            if response.status_code != 204:
                return response.raise_for_status()
            else:
                print(f"Correctly deleted org: {i['username']}")
    def delete_token(self, token="admin_token"):
        return requests.delete(f"{self.GITEA_URL}/users/{self.OWNER}/tokens/{token}",
                               auth=HTTPBasicAuth(self.OWNER, self.PASSWORD),
                               headers={"Accept": "application/json"}
                               )