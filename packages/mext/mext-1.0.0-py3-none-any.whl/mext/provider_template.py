import requests

from urllib.parse import urlparse

class Provider:

    def __init__(self, url):
        self.name = ''
        self.baseUrl = ''
        self.language = ''
        self.client = None
        self.session = requests.Session()
        self.login_success = False
        self.session_token = None
        self.refresh_token = None
        self.rate_limit = 0.25

        self.url = url
        self.parsed_url = urlparse(url)

    def get_manga(self):
        raise NotImplementedError

    def get_chapters(self):
        raise NotImplementedError

    def get_manga_chapters(self):
        raise NotImplementedError
