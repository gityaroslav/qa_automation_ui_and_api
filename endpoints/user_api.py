import requests


class UserAPI:

    def __init__(self, base_url="https://petstore.swagger.io/v2"):
        self.base_url = base_url
        self.user_endpoint = f"{self.base_url}/user"

    def create_user(self, user_data):
        headers = {
            "Content-type": "application/json",
            "accept": "application/json"
        }
        response = requests.post(self.user_endpoint, json=user_data, headers=headers)
        return response

    def update_user_by_username(self, username, updated_user_data):
        headers = {
            "Content-type": "application/json",
            "accept": "application/json"
        }
        url = f"{self.user_endpoint}/{username}"
        response = requests.put(url, json=updated_user_data, headers=headers)
        return response

    def get_user_by_username(self, username):
        url = f"{self.user_endpoint}/{username}"
        response = requests.get(url)
        return response

    def delete_user(self, username):
        url = f"{self.user_endpoint}/{username}"
        response = requests.delete(url)
        return response