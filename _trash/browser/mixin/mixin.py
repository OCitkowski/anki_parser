import json
from selenium.webdriver.chrome.options import Options
from _trash.browser.chrome_browser.options import CHROME_OPTIONS


class CookiesMixin:
    def __init__(self):

        super().__init__()

    @property
    def cookies_browser(self):
        return self.get_cookies()

    @cookies_browser.setter
    def cookies_browser(self, cookies_file_name):
        try:
            cookies_file = open(f"{self.__verifity_file_name(cookies_file_name)}.cookies", "r")
            cookies = json.load(cookies_file)
            for cookie in cookies:
                self.add_cookie(cookie)
        except:
            self.refresh()
        finally:
            # cookies_file.close()
            pass

    @cookies_browser.deleter
    def cookies_browser(self):
        self.delete_all_cookies()

    @staticmethod
    def __verifity_file_name(file_name: str):
        if isinstance(file_name, str):
            return file_name
        else:
            raise TypeError

    def save_cookies_to_file(self, cookies_file_name: str) -> bool:
        result = False
        try:
            with open(f"{cookies_file_name}.cookies", 'w') as write_file:
                json.dump(self.get_cookies(), write_file, ensure_ascii=False)
                result = True
            print(f'{cookies_file_name}.cookies save to root')
        except Exception as ex:
            print(f'{cookies_file_name}.cookies don`t save to root : {ex}')
        return result


class OptionsMixin:
    chrome_options_mixin = Options()

    def __init__(self):
        super().__init__()

    def set_chrome_options_mixin(self):
        for row in CHROME_OPTIONS:
            self.chrome_options_mixin.add_argument(row)

        return self.chrome_options_mixin
