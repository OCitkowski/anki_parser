from utils.anki_utils import invoke
from utils.redis_utils import get_from_redis_word_data, set_to_redis_word_data
from config.settings import PORT_REDIS, DB_URLS_RADIS, URL, DONOR_DECK_NAME

template = {
    'Deutsch': '',
    'Ukraine': '',
    'Wortarten': '',
    'Plural_Flexionsformen': '',
    'Bild': '',
    'Beispielsatz I': '',
    'Ukr Beispielsatz I': '',
    'Beispielsatz II': '',
    'Ukr Beispielsatz II': '',
    'Beispielsatz III': '',
    'Ukr Beispielsatz III': '',
    'Beispielsatz IV': '',
    'Ukr Beispielsatz IV': '',
    'Beispielsatz V': '',
    'Ukr Beispielsatz V': '',
    'Beispielsatz VI': '',
    'Ukr Beispielsatz VI': '',
    'Kommentar': '',
    'Zusätzlich': '',
    'Id': '',
    'URL': '',
    'Audio': '',
    'Status': False,
}


def get_deck_note_ids(deck_name=DONOR_DECK_NAME):
    if deck_name is None:
        return None
    else:
        try:
            note_ids = invoke('findNotes', query=f'deck:"{deck_name}"')
        except Exception as e:
            print(e)
            return None
    return note_ids


def get_deck_note(note_id=None):
    if note_id is None:
        return None
    else:
        try:
            note = invoke("notesInfo", notes=[note_id])
        except Exception as e:
            print(e)
            return None
    return note


def get_verb_data():
    data = []
    note_ids = get_deck_note_ids(deck_name=DONOR_DECK_NAME)

    for i, note_id in enumerate(note_ids):
        if i > 100:
            break
        note = get_deck_note(note_id=note_id)
        note_fields = note[0]['fields']

        if note_fields['Part of Speech']['value'] == 'verb' and len(
                note_fields['German']['value'].split(' ')) == 1:  # only 1 word

            row = dict(template)
            row['Deutsch'] = note_fields['German']['value']
            row['Id'] = note_fields['Thing']['value']
            row['URL'] = f"{URL}{note_fields['German']['value']}"
            data.append(row)

        else:
            continue

    return data


def get_urls_list(count_urls: int = 0) -> list:
    urls = []

    data = get_verb_data()

    for i, row in enumerate(data):
        if i < count_urls:
            set_to_redis_word_data(id=row['Id'], data=row, port=PORT_REDIS, db=DB_URLS_RADIS)
            r_row = get_from_redis_word_data(id=row['Id'], port=PORT_REDIS, db=DB_URLS_RADIS)
            urls.append(r_row['URL'])

    return urls


if __name__ == '__main__':
    urls = get_urls_list()
    for i, url in enumerate(urls):
        print(i, url)
