import json
import urllib.request


def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}


def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))
    # print(response)
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


def get_notes_info(deck_name):
    result = invoke('findNotes', query=f'deck:"{deck_name}" ')
    return result


def get_notes_deck():
    result = invoke('deckNames')
    deck_name = result[1]
    note_ids = invoke('findNotes', query=f'deck:"{deck_name}"')

    return note_ids


def retrieve_audio_file(filename):
    # filename = 'sound:google-85d48e18-99878f31-b3944b13-31678411-6325f384.mp3'
    audio_data = invoke('retrieveMedia', filename=filename)
    if audio_data:
        with open(filename, 'wb') as audio_file:
            audio_file.write(audio_data)
        print(f"Аудіофайл {filename} отримано та збережено на диск.")
    else:
        print(f"Не вдалося отримати аудіофайл {filename}.")


if __name__ == '__main__':
    print(invoke('deckNames'))
