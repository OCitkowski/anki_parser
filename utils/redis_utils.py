# redis
import json
import redis
from config.settings import NAME_JSON_WORDS_FILE, PORT_PROXY_REDIS, DB_PROXY_RADIS


# verbformen_parser
def set_to_redis_word_data(id: str, data, port: int, db: int):
    redis_client = redis.Redis(host='localhost', port=port, db=db)
    # серіалізація списку у JSON
    data_json = json.dumps(data)
    try:
        redis_client.set(id, data_json)
    except Exception as ex:
        print(ex)


def get_from_redis_word_data(id: str, port: int, db: int) -> dict:
    try:
        redis_client = redis.Redis(host='localhost', port=port, db=db)
        item = json.load(redis_client.get(id))
    except Exception as ex:
        print(ex)
    return item


# *****************************************************
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
