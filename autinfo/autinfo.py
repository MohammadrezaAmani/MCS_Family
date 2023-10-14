import re
from requests import session
from .html_tools import csrf, change_unicode


class AutInfo:
    """AUT Students information gatherer (idk this word has meaning or not)

    Functions:
        get: get a user
        get_range: get a range of users
    """

    URL = "https://samad.aut.ac.ir/index/index.rose"
    URL_MESSAGES = "https://samad.aut.ac.ir/messaging/searchUsers.rose?q=%s"
    URL_LOGIN = "https://samad.aut.ac.ir/j_security_check"

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        self.session = session()
        self.login()

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, value: str):
        self._username = value

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, value: str):
        self._password = value

    def login(self) -> bool:
        """login to `samad.aut.ac.ir`

        Returns:
            bool: login status
        """
        login_page = self.session.get(self.URL)
        csrf_token = csrf(login_page.text)
        del login_page
        data = {
            "_csrf": csrf_token,
            "username": self.username,
            "password": self.password,
            "login": "ورود",
        }
        try:
            self.session.post(self.URL_LOGIN, data=data)
            return True
        except Exception as e:
            print(e)
            return False

    def format_data(self, text: str) -> list:
        pattern = r"(\d{1,12})\(([^)]+)\)"
        matches = re.findall(pattern, text)
        student_info = [(match[0], match[1]) for match in matches]
        return student_info

    def get(self, student_id: int) -> list:
        return self.format_data(
            self.session.get(self.URL_MESSAGES % change_unicode(str(student_id))).text
        )

    def get_range(self, start: int, end: int) -> list:
        start, end = int(start), int(end)
        #! this function can be optimized but I'm so tired. :'(
        # TODO: with `self.get` you can get 10 number of queries and just customize that
        #! take care about the start and end of this function
        return [self.get(i)[0] for i in range(start, end + 1)]
