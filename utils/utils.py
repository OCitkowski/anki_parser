import json, os
from config.settings import URL


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


if __name__ == '__main__':
    pass
# del_empty_row()


# get_redis_words_trans_list()
# del_empty_row()
# redis_items = get_redis_words_trans_list()
#
# for i, j in redis_items.items():
#     print(i, j)
# print(get_sorted_rating_proxy_list())
