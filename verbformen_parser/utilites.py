import json, os
import redis
from verbformen_parser.settings import URL, NAME_JSON_WORDS_FILE, PORT_PROXY_REDIS, DB_PROXY_RADIS


# urls
def get_urls_from_file(json_file_words: str, count_items: int = None) -> list:
    urls = []
    for i, row in enumerate(get_data_from_json_file_words(json_file_words)):
        if count_items != None and i > count_items:
            break

        else:
            if row[2] == False:
                urls.append(f'{URL}{row[0]}?id={row[1]}&status={row[2]}')  # https://example.com/?name=John&age=30
    return urls


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
                                value['status'],
                                value['german_alternatives']
                                ])

    except Exception as ex:
        print(ex, os.path.abspath(__file__))

    return row


# cookies?
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
            # print(f'set cookies is {result}')
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
        # print(f'{cookies_file_name}.pkl save to root')
    except Exception as ex:
        print(f'{cookies_file_name}.pkl don`t save to root : {ex}')
    finally:
        write_file.close()

    return result


# json
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
    words = []
    try:

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


# redis
def get_sorted_rating_proxy_list():
    redis_client = redis.Redis(host='localhost', port=PORT_PROXY_REDIS, db=DB_PROXY_RADIS)
    rating_proxy_list = []
    sorted_rating_proxy_list = []
    keys = redis_client.keys()

    for key in keys:
        item_json = redis_client.get(key)
        rating_proxy_list.append(json.loads(item_json))

    # sorted_rating_proxy_list = sorted(rating_proxy_list, key=lambda item: item[1] - item[2], reverse=True)
    sorted_rating_list = sorted(rating_proxy_list, key=lambda x: (-x[1] + x[2], -x[1]))

    for i in sorted_rating_list:
        sorted_rating_proxy_list.append(i[0])

    return sorted_rating_proxy_list


def set_to_redis_words_trans_list(item, url_params):
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    # серіалізація списку у JSON
    item_url_params_json = json.dumps(item)

    try:
        redis_client.set(url_params['id'][0], item_url_params_json)
        print(f'{url_params["id"][0]} is OK')
    except:
        pass





def del_empty_row():
    redis_client = redis.Redis(host='localhost', port=6379, db=0)

    for key in redis_client.scan_iter():
        value = redis_client.get(key)
        if json.loads(value.decode())[0] == '':
            redis_client.delete(key)


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
                    value['translation'] = data[0]  # замінюємо значення "translation"
                    value['german_alternatives'] = data[0]
                    value['status'] = True  # змінюємо статус з False на True

        write_file.seek(0)
        json.dump(items_json, write_file, ensure_ascii=False, indent=4)
        write_file.truncate()


if __name__ == '__main__':
    # del_empty_row()
    save_from_redis_items_to_words('words.json')

    # get_redis_words_trans_list()
    # del_empty_row()
    # redis_items = get_redis_words_trans_list()
    #
    # for i, j in redis_items.items():
    #     print(i, j)
    # print(get_sorted_rating_proxy_list())
