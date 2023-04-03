import json


class CookiesMixin():
    def __init__(self):

        super().__init__()
        self._cookies_file_name = 'chrome'
        self.__open_cook_file = None

    @property
    def cookies_file_name(self):
        return self._cookies_file_name

    @cookies_file_name.setter
    def cookies_file_name(self, file_name: str):
        self._cookies_file_name = self.__verifity_file_name(file_name)


    @staticmethod
    def __verifity_file_name(file_name: str):
        if isinstance(file_name, str):
            return file_name
        else:
            raise TypeError





    def del_cookies_browser(self) -> bool:
        result = False
        try:
            self.__browser.delete_all_cookies()
            result = True
        except:
            self.__browser.refresh()

        return result

    def set_cookies_to_browser(self) -> bool:
        result = False
        try:
            self.__browser.delete_all_cookies()
            self.__open_cook_file = open(f"{self._cookies_file_name}.cookies", "r")
            cookies = json.load(self.__open_cook_file)
            for cookie in cookies:
                try:
                    self.__browser.add_cookie(cookie)
                    result = True
                    # print(cookie)
                except Exception as ex:
                    print(ex)
        except:
            self.__browser.refresh()
            result = False
        finally:

            self.__open_cook_file.close()
            print(f'set cookies is {result}')
            return result

    def save_cookies_to_file(self) -> bool:
        result = False
        try:
            print(self._cookies_file_name)

            with open(f"{self._cookies_file_name}.cookies", 'w') as write_file:
                json.dump(self.__browser.get_cookies(), write_file, ensure_ascii=False)
                result = True
            print(f'{self._cookies_file_name}.cookies save to root')
        except Exception as ex:
            print(f'{self._cookies_file_name}.cookies don`t save to root : {ex}')
        return result

class BrauserOptions():
    def __init__(self):
        self.__browser = None
        self.__chrome_options = ''
        self._json_file_name = 'chrome'

    @property
    def chrome_options(self):
        chrome_options = []
        for i in self.__chrome_options.arguments:
            chrome_options.append(i)
        return chrome_options

    @chrome_options.setter
    def chrome_options(self, options):
        self.__chrome_options.add_argument("--disable-extensions")
        for option in options:
            self.__chrome_options.add_argument(option)

        # self.__browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
        #                                   options=self.__chrome_options)

    @chrome_options.deleter
    def chrome_options(self):
        self.__chrome_options.arguments.clear()
