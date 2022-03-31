import fake_useragent
import requests
from bs4 import BeautifulSoup as BS

from errors import InternalError, NotAuthorizedError, NotFoundPageError
from parser import parse_week
from utils import timeout_ignore

class NZAPIConnection:
    def __init__(self):
        self.session = requests.session()
        self.session.verify = False
        self.session.trust_env = False

        user_agent = fake_useragent.UserAgent(verify_ssl=False).random

        self.headers = {
            "User-Agent": user_agent,
        }

    @timeout_ignore
    def get_csrf(self, page_url):
        response = self.session.get(url=page_url, headers=self.headers, timeout=0.4)
        page_bs = BS(response.content, 'html.parser')

        csrf1 = page_bs.find("input", {"name": "_csrf"})
        csrf2 = page_bs.find("meta", {"name": "csrf-token"})

        if csrf1:
            return csrf1["value"]
        if csrf2:
            return csrf2["content"]

        raise InternalError(msg="CSRF not found")

    @timeout_ignore
    def check_auth(self):
        response = self.session.get(url="https://nz.ua/", headers=self.headers, timeout=0.4)
        page_bs = BS(response.content, 'html.parser')
        auth_test_el = page_bs.find("form", {"id": "login-form"})

        return not auth_test_el

    @timeout_ignore
    def get_page(self, url):
        if not self.check_auth():
            raise NotAuthorizedError

        response = self.session.get(url=url, headers=self.headers)

        if response.status_code == 404:
            raise NotFoundPageError

        return BS(response.content, 'html.parser')

    @timeout_ignore
    def post(self, url, data):
        data["_csrf"] = self.get_csrf(url)
        self.headers["Referer"] = url
        self.session.post(url=url, data=data, headers=self.headers, timeout=0.4)

    def login(self, username, password):
        URL = "https://nz.ua"

        data = {
            "LoginForm[login]": username,
            "LoginForm[password]": password,
            "LoginForm[rememberMe]": "1"
        }

        self.post(url=URL, data=data)

        if not self.check_auth():
            raise NotAuthorizedError("Invalid login or password")

    def logout(self):
        URL = "https://nz.ua/logout"
        self.post(url=URL, data={})

example_user_data = {
    "username": "lupashko_dmitro2",
    "password": "985233gt"
}

def scrap_week(username, password, start_date):
    api_connection = NZAPIConnection()
    api_connection.login(username, password)

    page = api_connection.get_page("https://nz.ua/school5965/schedule/diary?start_date=" + start_date)
    week = parse_week(page)

    api_connection.logout()

    return week
