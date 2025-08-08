import os
import httpx


class UserAPI:

    def __init__(self, base_url="https://petstore.swagger.io/v2"):
        api_key = os.getenv("API_KEY")
        self.base_url = base_url
        self.user_endpoint = f"{self.base_url}/user"
        self.headers = {}
        if api_key:
            self.headers["api_key"] = api_key

    def create_user(self, user_data):
        headers = {
            "Content-type": "application/json",
            "accept": "application/json"
        }
        response = httpx.post(self.user_endpoint, json=user_data, headers=headers)
        return response

    def update_user_by_username(self, username, updated_user_data):
        headers = {
            "Content-type": "application/json",
            "accept": "application/json"
        }
        url = f"{self.user_endpoint}/{username}"
        response = httpx.put(url, json=updated_user_data, headers=headers)
        return response

    def get_user_by_username(self, username):
        url = f"{self.user_endpoint}/{username}"
        response = httpx.get(url)
        return response

    def delete_user(self, username):
        url = f"{self.user_endpoint}/{username}"
        response = httpx.delete(url)
        return response