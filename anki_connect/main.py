from anki_utils import invoke, get_notes_info

deck_name = 'Deutsch_Sätze'

def remove_duplicates(deck_name, field_name):
    notes = get_notes_info(deck_name)

    unique_notes = {}  # Словник для зберігання унікальних нотаток за значенням поля

    for note_id in notes:
        note = invoke('notesInfo', notes=[note_id])[0]
        fields = note['fields']
        deutsch_satz = fields.get(field_name, {}).get('value')

        if deutsch_satz not in unique_notes:
            unique_notes[deutsch_satz] = note_id
        else:
            # Видалити дублікат нотатки
            invoke('deleteNotes', notes=[note_id])
            print('Дублікати успішно видалено.', note_id)

if __name__ == '__main__':
    field_name_to_check = 'DeutschSatz'
    remove_duplicates(deck_name, field_name_to_check)






