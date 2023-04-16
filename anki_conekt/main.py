# https://github.com/FooSoft/anki-connect
# /home/fox/.config/google-chrome/Default
import json
import re
import urllib.request


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


if __name__ == '__main__':

    # назви колод
    result = invoke('deckNames')
    print('got list of decks: {}'.format(result))

    # Отримати список ID карток у колоді з іменем "MyDeckName"
    deck_name = result[1]
    note_ids = invoke('findNotes', query=f'deck:"{deck_name}"')
    print(f'Знайдено {len(note_ids)} карток у колоді {deck_name}')

    # Замінити поле "MyFieldName" на "NewFieldValue" в усіх картках
    field_name1 = 'Part of Speech'
    field_name2 = 'Level'

    new_field_value = 'NewFieldValue'
    for i, note_id in enumerate(note_ids):
        # if i > 100:
        #     break
        note_info = invoke('notesInfo', notes=[note_id])[0]

        # note_info['tags'].clear()
        # invoke('updateNoteTags', note=note_info['noteId'], tags=note_info['tags'])

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

            # invoke('updateNoteFields', note=note_info['noteId'], tags=note_info['tags'])

        # Зберегти зміни в Anki

        #
        # print(note_id, note_info['fields'][field_name]['value'], note_info['tags'])
        # print(note_info['fields'][field_name]['value'] in note_info['tags'])

        # if field_name in note_info['fields']:
        #     note_info['fields'][field_name] = new_field_value
        #     invoke('updateNoteFields', note={'id': note_info['noteId'], 'fields': note_info['fields']})
        #     print(f'Замінено поле "{field_name}" на "{new_field_value}" в картці з ID {note_id}')
        # else:
        #     print(f'Поле "{field_name}" відсутнє в картці з ID {note_id}')

# 1421053850741 {'noteId': 1421053850741, 'tags': ['Level015'], 'fields':{
#     'German': {'value': 'bekannt', 'order': 0},
#     'Picture': {'value': '<img src="paste-28140625723393.jpg" />', 'order':
#     1},'English': {'value': 'well-known', 'order':
#     2}, 'Audio': {'value': '[sound:aa9c8cb0-9f97-579e-8d05-7a2f9c4b6702.mp3]', 'order':
#     3}, 'Sample sentence': {'value': 'Heike Makatsch ist eine bekannte deutsche Schauspielerin.', 'order': 4},
#     'Plural and inflected forms': {'value': '', 'order': 5}, 'German Alternatives': {'value': '', 'order': 6},
#     'English Alternatives': {'value': '', 'order':
#         7}, 'Part of Speech': {'value': 'adj', 'order':
#         8}, 'Level': {'value': '15', 'order':
#         9}, 'Thing': {'value': '23720117', 'order':
#         10}}, 'modelName': 'Memrise - 4000 German Words by Frequency-7eb67-110c6', 'cards': [1421053850742, 1421592707928]}
