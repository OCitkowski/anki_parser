# https://github.com/FooSoft/anki-connect
# /home/fox/.config/google-chrome/Default
import json
import re
import urllib.request
import redis

redis_client_7 = redis.Redis(host='localhost', port=6379, db=7)
words_json = '/home/fox/PycharmProjects/anki_parser/verbformen_parser/words.json'


def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}


def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']


def get_notes_deck():
    result = invoke('deckNames')
    deck_name = result[1]
    note_ids = invoke('findNotes', query=f'deck:"{deck_name}"')

    return note_ids


def update_deck():
    pass


def add_json_data_to_redis():
    # Отримуємо дані з файлу JSON
    with open(words_json, 'r') as f:
        json_data = json.load(f)

    # Додаємо дані до Redis бази даних
    for d in json_data:
        for k, v in d.items():
            # Отримуємо ключ
            id_ = v.get('id')

            # Додаємо дані до Redis
            redis_client_7.set(id_, json.dumps(v))


def get_data_from_redis(id_):
    data = redis_client_7.get(id_)
    if data:
        return json.loads(data.decode('utf-8'))
    return None


def get_redis_words_trans_list():
    result = {}
    try:

        for key in redis_client_7.scan_iter("*"):
            value = redis_client_7.get(key)
            result[key.decode()] = json.loads(value.decode())
    except Exception as ex:
        print(ex)

    return result


# *****************************************************
def add_tag():
    # add tag  в усіх картках
    field_name1 = 'Part of Speech'
    field_name2 = 'Level'

    new_field_value = 'NewFieldValue'
    for i, note_id in enumerate(None):

        note_info = invoke('notesInfo', notes=[note_id])[0]

        try:
            x = int(note_info['fields'][field_name2]['value'])

            tag = note_info['fields'][field_name1]['value']
            tag1 = re.sub(r'\d+\)|\(|\)+-1234567890.;:,', '', tag)

            tag2 = f'{x:03d}'
            note_info['tags'].append(tag2)
            note_info['tags'].append(tag1)
            invoke('updateNoteTags', note=note_info['noteId'], tags=note_info['tags'])
        except:
            pass


def old_main():
    add_json_data_to_redis()
    # for i, row in get_redis_words_trans_list().items():
    #     if row['status']:
    #         print(i, row)
    note_ids = get_notes_deck()

    ids = []
    for i, note_id in enumerate(note_ids):

        # if i > 10 or note_id == None:
        #     break
        note = invoke("notesInfo", notes=[note_id])
        note_fields_t_v = note[0]['fields']['Thing']['value']

        data = get_data_from_redis(note_fields_t_v)

        if data == None:
            continue

        if data['status'] == False:
            continue

        ids.append(note_id)

        Ukrainisch = data['translation']

        invoke('updateNoteFields', note={'id': int(note_id), 'fields': {'Ukrainisch': Ukrainisch}})
        print(i, note_id, Ukrainisch)

        invoke('addTags', notes=[note_id], tags='ukr')


# addTags


if __name__ == '__main__':
    # print(invoke('deckNames'))
    deck_name = 'Deutsch: 4000 German Words by Frequency - WD Updated 5 Feb 2023'
    note_ids = invoke('findNotes', query=f'deck:"{deck_name}"')
    for i, note_id in enumerate(note_ids):
        if i > 100:
            break
        # print(i, note_id)
        note = invoke("notesInfo", notes=[note_id])
        note_fields = note[0]['fields']
        # print(note_fields['Part of Speech']['value'])
        if note_fields['Part of Speech']['value'] == 'verb' and len(note_fields['German']['value'].split(' ')) == 1:
            print(note_fields['Thing']['value'], note_fields['German']['value'])
            print(note_fields)

    # old_main()
