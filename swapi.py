import requests
import os


class APIRequester:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self):
        url = self.base_url
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f'Ошибка при выполнении запроса: {e}')
            return None


class SWRequester(APIRequester):
    def __init__(self):
        super().__init__("https://swapi.dev/api/")

    def get_sw_categories(self):
        response = self.get()
        if response:
            return list(response.json().keys())
        return []

    def get_sw_info(self, sw_type):
        response = self.get(sw_type)
        if response:
            return response.text
        return None


def save_sw_data():
    sw_requester = SWRequester()
    categories = sw_requester.get_sw_categories()

    if not os.path.exists('data'):
        os.makedirs('data')

    for category in categories:
        data = sw_requester.get_sw_info(category)
        if data:
            with open(f'data/{category}.txt', 'w') as file:
                file.write(data)
