import json
import urllib.request


def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}


def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))
    print(response)
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']


def add_note_to_deck(deutsch, ukr, deck_name, modelName):
    # Спочатку створіть нотатку з необхідними полями та колодою
    note_data = {
        'deckName': deck_name,
        'modelName': modelName,
        'fields': {
            'Deutsch': deutsch,
            'Ukr': ukr
        }
    }
    result = invoke('addNote', note=note_data)
    print(result)

    # Поверніть ідентифікатор нової нотатки
    return result


def get_notes_deck():
    result = invoke('deckNames')
    deck_name = result[1]
    note_ids = invoke('findNotes', query=f'deck:"{deck_name}"')

    return note_ids


if __name__ == '__main__':
    print(invoke('deckNames'))
