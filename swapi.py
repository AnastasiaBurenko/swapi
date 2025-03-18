import requests
from pathlib import Path


class APIRequester:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint=""):
        try:
            url = f'{self.base_url}{endpoint}'
            response = requests.get(url)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            error_message = f'Возникла ошибка при выполнении запроса {e}'
            print(error_message)


class SWRequester(APIRequester):
    def __init__(self, base_url='https://swapi.dev/api/'):
        super().__init__(base_url)

    def get_sw_categories(self):
        if not self.base_url.endswith('/'):
            self.base_url += '/'
        response = self.get()
        categories = response.json()
        return categories.keys()

    def get_sw_info(self, sw_type):
        self.url = self.base_url + '/' + sw_type + '/'
        response = requests.get(self.url)
        return response.text


def save_sw_data(base_url='https://swapi.dev/api'):
    sw_requester = SWRequester(base_url)
    categories = sw_requester.get_sw_categories()

    directory_path = Path('data')
    directory_path.mkdir(exist_ok=True)

    for category in categories:
        data = sw_requester.get_sw_info(category)
        if data:
            with open(f'data/{category}.txt', 'w', encoding='utf-8') as file:
                file.write(data)
