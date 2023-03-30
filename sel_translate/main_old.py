import os, time, random, json
from datetime import datetime
import logging

from dotenv import load_dotenv

from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.common.by import By

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

from webdriver_manager.chrome import ChromeDriverManager
from browser_options import CHROME_OPTIONS
import redis

r = redis.Redis()
r.ping()

load_dotenv()
password = os.getenv("PASSWORD")
user_name = os.getenv("USER_NAME")


def get_proxies_txt(filename):
    with open(filename + '.txt', 'r') as f:

        lines = f.readlines()
        # Відфільтровуємо перший рядок, який містить назву та дату
        lines = [line.strip() for line in lines if 'Free proxies' not in line and 'Updated' not in line]
        # Перетворюємо решту рядків з файлу на список проксі
        proxies = [line.strip() for line in lines if line.strip()]
    print(proxies)
    return proxies

class ChromeBrowser():
    """Chrome __browser"""
    __type = "ChromeBrowser"

    def __init__(self):
        self.__browser = None
        self.__chrome_options = Options()
        self._cookies_file_name = 'chrome'
        self.__open_cook_file = None
        self._json_file_name = 'chrome'
        self.__max_time_sleep = 0
        self.__min_time_sleep = 0
        self.__hand_time_sleep = 0

    def __del__(self):
        if self.__browser:
            self.__close()

    def __str__(self):
        return f"Chrome __browser: {self.__browser} Timing: max = {self.__max_time_sleep}  min = {self.__min_time_sleep}  hand = {self.__hand_time_sleep}"

    @staticmethod
    def __verifity_time_sleep(time_sleep: int):
        if isinstance(time_sleep, int):
            return time_sleep
        else:
            raise TypeError

    @staticmethod
    def __verifity_file_name(file_name: str):
        if isinstance(file_name, str):
            return file_name
        else:
            raise TypeError

    @staticmethod
    def print_type():
        print(ChromeBrowser.__type)

    def get_times_sleep(self) -> dict:
        return {'hand_time': self.__hand_time_sleep, 'min': self.__min_time_sleep, 'max': self.__max_time_sleep}

    def set_times_sleep(self, hand_time_sleep: int = 0, min_time_sleep: int = 0, max_time_sleep: int = 0):
        if self.__verifity_time_sleep(hand_time_sleep) > 0:
            self.__hand_time_sleep = hand_time_sleep
            self.__min_time_sleep = 0
            self.__max_time_sleep = 0

        if self.__verifity_time_sleep(hand_time_sleep) == 0 \
                and self.__verifity_time_sleep(min_time_sleep) <= self.__verifity_time_sleep(max_time_sleep):
            self.__min_time_sleep = min_time_sleep
            self.__max_time_sleep = max_time_sleep

    @property
    def cookies_file_name(self):
        return self._cookies_file_name

    @cookies_file_name.setter
    def cookies_file_name(self, file_name: str):
        self._cookies_file_name = self.__verifity_file_name(file_name)

    @cookies_file_name.deleter
    def cookies_file_name(self):
        self._cookies_file_name = ''

    @property
    def json_file_name(self):
        return self._json_file_name

    @json_file_name.setter
    def json_file_name(self, file_name: str):
        self._json_file_name = self.__verifity_file_name(file_name)

    @json_file_name.deleter
    def json_file_name(self):
        self._json_file_name = ''

    @property
    def chrome_options(self):
        chrome_options = []
        for i in self.__chrome_options.arguments:
            chrome_options.append(i)
        return chrome_options

    @chrome_options.setter
    def chrome_options(self, options):

        proxies = get_proxies_txt('free_proxy')  # список проксі

        # options = webdriver.ChromeOptions()

        for proxy in proxies:
            self.__chrome_options.add_argument('--proxy-server={}'.format(proxy))  # додаємо кожен проксі до налаштувань

        # driver = webdriver.Chrome(options=options)

        self.__chrome_options.add_argument("--disable-extensions")
        for option in options:
            self.__chrome_options.add_argument(option)

        self.__browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                          options=self.__chrome_options)

    @chrome_options.deleter
    def chrome_options(self):
        self.__chrome_options.arguments.clear()

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

    def save_data_in_json_file(self, data):
        result = False
        try:
            with open(self._json_file_name + '.json', 'w') as write_file:
                json.dump(data, write_file, ensure_ascii=False)
                result = True
            print(f'{self._json_file_name}.json save to root')
        except:
            print(f'{self._json_file_name}.json don`t save to root')
        return result

    def get_data_from_json_file(self):
        result = False
        try:
            with open(self._json_file_name + '.json', 'r') as read_file:
                result = json.load(read_file)
            print(f'{self._json_file_name}.json get data from json file')
        except:
            print(f'{self._json_file_name}.json don`t get data from json file')
        return result

    def open(self):
        return self.__browser

    def sleep(self):
        if self.__hand_time_sleep > 0:
            time.sleep(self.__hand_time_sleep)
        else:
            time.sleep(random.randrange(self.__min_time_sleep, self.__max_time_sleep))

    def xpath_exists(self, xpath):
        try:
            self.__browser.find_element(By.XPATH, xpath)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    def __close(self):

        self.__browser.close()


class TranslateBot(ChromeBrowser):
    """Translate Bot"""
    __type = "Translate"

    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password
        self.__link_by_default = 'https://dict.com/%D0%BD%D1%96%D0%BC%D0%B5%D1%86%D1%8C%D0%BA%D0%BE-%D1%83%D0%BA%D1%80%D0%B0%D1%96%D0%BD%D1%81%D1%8C%D0%BA%D0%B8%D0%B8/hallo'

    def open_by_word(self):
        self.__browser = self.open()
        if not self.__link_by_default == None:
            self.__browser.get(self.__link_by_default)
            self.set_cookies_to_browser()
            # self.__browser.refresh()
            self.sleep()

    def put_word_to_element(self, word: str = None):
        if word != None and word != ' ':
            word_element = self.__browser.find_element(By.XPATH,
                                                       '/ html / body / div[1] / div[2] / div / div[1] / div / form / input[1]')
            word_element.clear()
            self.__browser.refresh
            self.sleep()

            word_element.send_keys(word)
            print(f'{word} ------')
            word_element.send_keys(Keys.ENTER)
            self.sleep()

    def find_elements_by_css_old(self, element_css_names: list) -> dict:
        finded_elements = {}

        try:
            seach_elements_head = self.__browser.find_element(By.CLASS_NAME, 'head')
        except:
            return None

        for i in element_css_names:
            try:
                finded_elements[i] = seach_elements_head.find_element(By.CSS_SELECTOR, i).text
            except:
                # print(f'{i} this is css did not find - {i}')
                finded_elements[i] = None
            finally:
                self.sleep()

        # for i, j in finded_elements.items():
        #     print(i, j)

        return finded_elements

    def find_elements_by_css(self, element_css_names: list) -> dict:
        finded_elements = {}

        for i in element_css_names:
            try:
                full_row = ''
                elements = self.__browser.find_elements(By.CSS_SELECTOR, i)
                for row in elements:
                    full_row += f'{row.text}; '

                finded_elements[i] = full_row
            except:

                finded_elements[i] = None
            finally:
                self.sleep()

        return finded_elements

    def find_elements_by_css_to_list(self, element_css_names: list) -> list:
        finded_elements = []

        for i in element_css_names:
            try:
                full_row = ''
                elements = self.__browser.find_elements(By.CSS_SELECTOR, i)
                for row in elements:
                    full_row += f'{row.text}; '

                finded_elements.append(full_row)
            except:

                finded_elements.append(' ')
            finally:
                self.sleep()

        return finded_elements


def get_words_from_file(full_file_name: str = None) -> list:
    words = []

    if full_file_name == None:
        return words

    file_txt = open(full_file_name, "r+")

    while True:
        row = file_txt.readline()
        if row == '':
            break
        else:
            new_word = row.split("|")[0]
            words.append(new_word)

    # r1 = redis.Redis(db=1)
    # r1.set(name='words', value=json.dumps(words))
    # print(json.loads(r1.get('words')))
    # return json.loads(r1.get('words'))
    return words


def get_data_from_json_file(json_file_name):
    try:
        with open(json_file_name + '.json', 'r') as read_file:
            template = json.load(read_file)
            logging.info(f"{json_file_name}.json get data from json file")
            words = (note['fields'][0] for note in template['notes'])
    except Exception as e:
        logging.info(f"{json_file_name}.json don`t get data from json file | {e}")

    return words


def get_data_from_json_file2(json_file_name):
    try:
        with open(json_file_name, 'r') as read_file:
            template = json.load(read_file)
            logging.info(f"{json_file_name}.json get data from json file")
    except Exception as e:
        logging.info(f"{json_file_name}.json don`t get data from json file | {e}")

    return template

def save_row_in_json_file(data, json_file_name):

    try:
        with open(json_file_name, 'w') as write_file:
            json.dump(data, write_file, ensure_ascii=False)
            result = True
        print(f'{json_file_name}.json save to root')
    except:
        print(f'{json_file_name}.json don`t save to root')
    return result

def update_row_in_json_file(id, row, json_file_name):
    # Відкрити файл xxx.json і зчитати дані в об'єкт Python
    with open(json_file_name) as f:
        data = json.load(f)

    # Знайти стрічку, яку потрібно змінити, і замінити на нову
    data[id][1] = row
    data[id][4] = True

    # Зберегти зміни в файл
    with open(json_file_name, 'w') as f:
        json.dump(data, f)



if __name__ == '__main__':

    logging.basicConfig(filename='_main.log', encoding='utf-8', datefmt='%Y-%m-%d_%H-%M-%S', level=logging.INFO)

    translate = TranslateBot(username=user_name, password=password)
    translate.cookies_file_name = user_name + '_translate'
    translate.set_times_sleep(hand_time_sleep=0, min_time_sleep=1, max_time_sleep=2)
    translate.chrome_options = CHROME_OPTIONS
    translate.open_by_word()

    element_class_names = (
        "span.lex_ful_tran", "span.lex_ful_entr.l1", "span.lex_ful_pron", "span.lex_ful_morf",
        "span.lex_ful_form")

    data = get_data_from_json_file2(json_file_name='data.json')

    i = 0
    print(datetime.now())
    for id, row in data.items():
        print(i)
        if row[4]:
            continue
        i += 1
        if i > 1000:
            break

        translate.put_word_to_element(row[0])

        finded_elements = translate.find_elements_by_css_to_list(element_class_names)

        if finded_elements == None:

            update_row_in_json_file(id, None, json_file_name='data.json')

            logging.FATAL(f'for {row[0]} did not found - {finded_elements}')

        else:
            update_row_in_json_file(id, finded_elements, json_file_name='data.json')
            logging.info(f'{i} + {datetime.now()}- for {row[0]} found - {finded_elements}')
            print(finded_elements)

    translate.save_cookies_to_file()
    print(datetime.now())
