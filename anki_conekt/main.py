#https://github.com/FooSoft/anki-connect
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


if __name__ == '__main__':
    #
    # add_json_data_to_redis()
    # for i, row in get_redis_words_trans_list().items():
    #     if row['status']:
    #         # print(i, row)

    note_ids = get_notes_deck()
    # print(note_ids)

    for i, note_id in enumerate(note_ids):
        if i > 1 or note_id == None:
            break
        note = invoke("notesInfo", notes=[note_id])
        print(note)
        print(note[0])
        print(note[0]['fields'])
        note_fields = note[0]['fields']
        note_fields_t_v = note[0]['fields']['Thing']['value']

        print(note_fields_t_v)
        data = get_data_from_redis(note_fields_t_v)

        if data == None:
            continue

        invoke('updateNoteFields', note=note[0])



        # note_info['fields']['Ukrainisch']['value'] = data['translation']
        # # Викликаємо функцію AnkiConnect для оновлення картки
        # # print(note_info['noteId'], type(note_info['fields']))
        # #
        # # new_fields = json.dumps(note_info['fields'])
        # # print(new_fields)
        # new_fields = {'Ukrainisch': 'новий текст на передній стороні'}
        # ew_fields_str = '\x1f'.join([f"{key}::{value}" for key, value in new_fields.items()])
        #
        # invoke('updateNoteFields', note=note_id, fields=ew_fields_str)


        # note_info = invoke("notesInfo", notes=[note_id])[0]
        # note_info['fields']['Ukrainisch'] = 'новий текст на передній стороні'
        #
        # invoke('updateNoteFields', note=json.dumps({'id': note_info['noteId'], 'fields': note_info['fields']}))
        # note_info = invoke("notesInfo", notes=[note_id])[0]

        # змінюємо значення поля Ukrainian
        note_fields['Ukrainisch']['value'] = 'новий текст на передній стороні'
        print(type(note_fields))
        # print( note_info['fields']['Ukrainisch'])
        # print(note_info['fields']['Ukrainisch']['value'])
        # print(note_info['fields'])

        # передаємо змінену інформацію про картку у функцію invoke
        # invoke('updateNoteFields', note_id=[note_id], = note_fields)
        #
        # invoke('updateNoteFields', note=json.dumps({'id': int(note_info['noteId']), 'fields': note_info['fields']}))





