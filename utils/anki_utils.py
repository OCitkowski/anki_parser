import json
import urllib.request

template = [
    {'Deutsch': ''},
    {'Ukraine': ''},
    {'Wortarten': ''},
    {'Plural_Flexionsformen': ''},
    {'Bild': ''},
    {'Beispielsatz I': ''},
    {'Ukr Beispielsatz I': ''},
    {'Beispielsatz II': ''},
    {'Ukr Beispielsatz II': ''},
    {'Beispielsatz III': ''},
    {'Ukr Beispielsatz III': ''},
    {'Beispielsatz IV': ''},
    {'Ukr Beispielsatz IV': ''},
    {'Beispielsatz V': ''},
    {'Ukr Beispielsatz V': ''},
    {'Beispielsatz VI': ''},
    {'Ukr Beispielsatz VI': ''},
    {'Kommentar': ''},
    {'Zusätzlich': ''},
    {'Id': ''},
    {'URL': ''},
    {'Audio': ''},
    {'Status': False},
]


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


if __name__ == '__main__':
    # print(invoke('deckNames'))
    deck_name = 'Deutsch: 4000 German Words by Frequency - WD Updated 5 Feb 2023'
    note_ids = invoke('findNotes', query=f'deck:"{deck_name}"')
    for i, note_id in enumerate(note_ids):
        if i > 1000:
            break
        # print(i, note_id)
        note = invoke("notesInfo", notes=[note_id])
        note_fields = note[0]['fields']
        # print(note_fields['Part of Speech']['value'])
        if note_fields['Part of Speech']['value'] == 'verb' and len(note_fields['German']['value'].split(' ')) == 1:
            print(note_fields['Thing']['value'], note_fields['German']['value'])
