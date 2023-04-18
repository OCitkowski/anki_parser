from utils.anki_utils import invoke

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

if __name__ == '__main__':
    deck_name = 'Deutsch: 4000 German Words by Frequency - WD Updated 5 Feb 2023'
    note_ids = invoke('findNotes', query=f'deck:"{deck_name}"')
    for i, note_id in enumerate(note_ids):
        if i > 100:
            break

        note = invoke("notesInfo", notes=[note_id])
        note_fields = note[0]['fields']

        if note_fields['Part of Speech']['value'] == 'verb' and len(note_fields['German']['value'].split(' ')) == 1:
            data = template
            data['Deutsch'] = note_fields['German']['value']
            data['Id'] = note_fields['Thing']['value']
        else:
            continue

        print(data)
