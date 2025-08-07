import requests


class PetAPI:

    def __init__(self, base_url="https://petstore.swagger.io/v2", api_key=None):
        self.base_url = base_url
        self.pet_endpoint = f"{self.base_url}/pet"
        if api_key:
            self.headers["api_key"] = api_key  # Add API key to headers if provided

    def create_pet(self, pet_data):
        headers = {
            "Content-type": "application/json",
            "accept": "application/json"
        }
        response = requests.post(self.pet_endpoint, json=pet_data, headers=headers)
        return response

    def update_pet(self, pet_data):
        headers = {
            "Content-type": "application/json",
            "accept": "application/json"
        }
        response = requests.put(self.pet_endpoint, json=pet_data, headers=headers)
        return response

    def get_pet_by_id(self, pet_id):
        url = f"{self.pet_endpoint}/{pet_id}"
        response = requests.get(url)
        return response

    def get_pet_by_status(self, status):
        url = f"{self.pet_endpoint}/findByStatus"
        headers = {
            "Content-type": "application/json",
            "accept": "application/json"
        }
        params = {"status": status}
        response = requests.get(url, params=params, headers=headers)
        return response

    def delete_pet(self, pet_id):
        url = f"{self.pet_endpoint}/{pet_id}"
        headers = {
        }
        response = requests.delete(url, headers=headers)
        return response
