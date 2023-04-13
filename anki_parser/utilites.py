import json, os, requests
import time

from selenium.webdriver.common.by import By

import redis
from anki_parser.settings import URL, NAME_JSON_WORDS_FILE


def get_urls_from_file(json_file_words: str, count_items: int = None) -> list:
    urls = []
    for i, row in enumerate(get_data_from_json_file_words(json_file_words)):
        if count_items != None and i > count_items:
            break

        else:
            if row[2] == False:
                urls.append(f'{URL}{row[0]}?id={row[1]}&status={row[2]}')  # https://example.com/?name=John&age=30
    return urls


def set_cookies_to_browser(driver, cookies_file_name) -> bool:
    result = False
    try:
        driver.delete_all_cookies()
        open_cook_file = open(f"{cookies_file_name}.pkl", "r")
        cookies = json.load(open_cook_file)
        for cookie in cookies:
            try:
                driver.add_cookie(cookie)
                result = True
            except Exception as ex:
                print(ex)
    except:
        driver.refresh()
        result = False

    finally:
        try:
            open_cook_file.close()
            print(f'set cookies is {result}')
        except Exception as ex:
            print(ex)

    return result


def save_cookies_to_file(driver, cookies_file_name) -> bool:
    result = False
    try:
        # print(cookies_file_name)

        with open(f"{cookies_file_name}.pkl", 'w') as write_file:
            json.dump(driver.get_cookies(), write_file, ensure_ascii=False)
            result = True
        print(f'{cookies_file_name}.pkl save to root')
    except Exception as ex:
        print(f'{cookies_file_name}.pkl don`t save to root : {ex}')
    finally:
        write_file.close()

    return result


def save_data_in_json_file(data, json_file_name):
    result = False
    try:
        with open(json_file_name, 'w') as write_file:
            json.dump(data, write_file, ensure_ascii=False, indent=2)
            result = True
        print(f'{json_file_name}.json save to root')
    except:
        print(f'{json_file_name}.json don`t save to root')
    return result


def get_data_from_json_file_deck(json_file_name):
    try:
        words = []
        with open(json_file_name + '.json', 'r+') as read_file:
            template = json.load(read_file)
            for i, note in enumerate(template['notes']):

                len_row = len(note['fields'][0].split(' '))
                row = note['fields'][0].split(' ')

                if len_row > 2:
                    continue

                if row[0] in ['der', 'Der', 'die', 'das'] and len_row != 2:
                    continue

                words.append(
                    {i: {
                        "word": note['fields'][0],
                        "id": note['fields'][12],
                        "translation": '',
                        "part_of_speech": note['fields'][10],
                        "german_alternatives": '',
                        "status": False
                    }})

    except:
        pass

    return words


def get_data_from_json_file_words(json_file_name):
    row = []

    try:
        with open(json_file_name, 'r') as file:
            data = json.load(file)

        for item in data:
            for key, value in item.items():

                if value['status'] == False:
                    row.append([value['word'],
                                value['id'],
                                value['status']])

    except Exception as ex:
        print(ex, os.path.abspath(__file__))

    return row


def save_item_in_json_file_old(item, json_file_name, url_params):
    write_file = open(json_file_name, "r+")

    try:
        items = json.load(write_file)
    except ValueError:
        items = []

    for dict_item in items:
        for key, value in dict_item.items():
            if value['id'] == url_params['id']:
                value['translation'] = item[0]  # замінюємо значення "translation"
                value['status'] = True

    # перемотка файлу на початок
    write_file.seek(0)

    # запис у вихідний файл
    json.dump(items, write_file, ensure_ascii=False, indent=4)

    # обрізання файлу, щоб він був тільки такого ж розміру, як вміщує даних
    write_file.truncate()

    write_file.close()


def find_elements_by_css(self, element_css_names: list) -> dict:
    # finded_elements = {}
    #
    # for i in element_css_names:
    #     try:
    #         full_row = ''
    #         elements = self.__browser.find_elements(By.CSS_SELECTOR, i)
    #         for row in elements:
    #             full_row += f'{row.text}; '
    #
    #         finded_elements[i] = full_row
    #     except:
    #
    #         finded_elements[i] = None
    #     finally:
    #         self.sleep()
    #
    # return finded_elements
    pass


def find_elements_by_css_to_list(driver, element_css_names: list) -> list:
    finded_elements = []

    for i in element_css_names:
        try:
            full_row = ''
            elements = driver.find_elements(By.CSS_SELECTOR, i)
            for row in elements:
                full_row += f'{row.text}; '

            finded_elements.append(full_row)
        except:

            finded_elements.append(' ')
        finally:
            time.sleep(5)

    return finded_elements


def check_proxy(proxy):
    try:
        response = requests.get('https://www.google.com', proxies={'https': proxy.rstrip('\n')},
                                timeout=1)
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return False


def set_to_redis_proxy_list(proxy_list: list, name_redis_proxy_list: str) -> None:
    r = redis.Redis(host='localhost', port=6379, db=0)
    try:
        for proxy in proxy_list:
            if check_proxy(proxy):
                r.rpush(name_redis_proxy_list, proxy)
                print(f'{proxy} redis OK')
            else:
                print(f'{proxy} redis failed')
    except:
        pass


def set_to_redis_words_trans_list(item, url_params):
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    # серіалізація списку у JSON
    item_url_params_json = json.dumps(item)

    try:
        redis_client.set(url_params['id'][0], item_url_params_json)
        print(f'{url_params["id"][0]} is OK')
    except:
        pass


def save_from_redis_items_to_words(json_file_name=NAME_JSON_WORDS_FILE):
    redis_client = redis.Redis(host='localhost', port=6379, db=0)

    with open(json_file_name, "r+") as write_file:
        try:
            items_json = json.load(write_file)
        except ValueError:
            items_json = []

        for dict_item in items_json:
            for key, value in dict_item.items():

                item_redis = redis_client.get(value['id'])
                if item_redis == None:
                    continue
                data = json.loads(item_redis.decode())

                if item_redis:
                    # print(data, type(data))
                    # print(data[0], type(data[0]))
                    value['translation'] = data[0]  # замінюємо значення "translation"
                    value['status'] = True  # змінюємо статус з False на True
                    print(data)

        write_file.seek(0)
        json.dump(items_json, write_file, ensure_ascii=False, indent=4)
        write_file.truncate()


if __name__ == '__main__':
    # pass
    # redis_client = redis.Redis(host='localhost', port=6379, db=0)

    # prefix = ""
    # keys = redis_client.keys(f"{prefix}*")
    # items = redis_client.mget(keys)
    # for i, row in enumerate(items):
    #     print(i, row)

    save_from_redis_items_to_words('words.json')

# words = get_data_from_json_file_deck('deck')
#
# save_data_in_json_file(words, 'words.json')
#
# file_json = '/home/fox/PycharmProjects/python_parsing/scrapy/dict_com/dict_com/spiders/words.json'
# words = get_data_from_json_file_words(file_json)
# for row in words:
#     # if row != None:
#     print(row[1])
#
# start_urls = [f"https://dict.com/ukrainisch-deutsch/{row}" for row in words]
