import json


class CookiesMixin:
    def __init__(self):
        #
        self._cookies_file_name = 'chrome'
        super().__init__()

    @property
    def cookies_file_name(self):
        return self._cookies_file_name

    @cookies_file_name.setter
    def cookies_file_name(self, file_name: str):
        self._cookies_file_name = file_name

    @property
    def cookies_browser(self):
        return self.get_cookies()

    @cookies_browser.setter
    def cookies_browser(self, clearn_old_cookies):
        try:

            if clearn_old_cookies:
                del (self.cookies_browser)

            cookies_file = open(f"{self.__verifity_file_name(self.cookies_file_name)}.cookies", "r")
            cookies = json.load(cookies_file)
            for cookie in cookies:
                try:
                    self.add_cookie(cookie)
                    print(f'set cookies from {self.cookies_file_name}')

                except Exception as ex:
                    print(ex)
        except:
            self.refresh()
        finally:
            cookies_file.close()

    @cookies_browser.deleter
    def cookies_browser(self):
        self.delete_all_cookies()

    @staticmethod
    def __verifity_file_name(file_name: str):
        if isinstance(file_name, str):
            return file_name
        else:
            raise TypeError

    def save_cookies_to_file(self) -> bool:
        result = False
        try:
            with open(f"{self.cookies_file_name}.cookies", 'w') as write_file:
                json.dump(self.get_cookies(), write_file, ensure_ascii=False)
                result = True
            print(f'{self.cookies_file_name}.cookies save to root')
        except Exception as ex:
            print(f'{self.cookies_file_name}.cookies don`t save to root : {ex}')
        return result
