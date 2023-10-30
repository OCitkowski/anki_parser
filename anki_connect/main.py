# https://github.com/FooSoft/anki-connect
# /home/fox/.config/google-chrome/Default
from anki_utils import invoke

deck_name = 'Satze'
modelName = 'Satze'  # Вкажіть модель, яку ви використовуєте в Anki


def add_note_to_deck(note_fields):
    # Спочатку створіть нотатку з необхідними полями та колодою
    note_data = {
        'deckName': deck_name,
        'modelName': modelName,
        'fields': note_fields  # Поля вашої нотатки
    }
    result = invoke('addNote', note=note_data)
    print(result)

    # Поверніть ідентифікатор нової нотатки
    return result['result']


if __name__ == '__main__':
    # Ваша колода та дані для нотатки

    note_fields = {
        'Deutsch': 'значення132',
        'Ukr': 'значення232'
        # Додайте інші поля та значення, які вам потрібні
    }

    # Додайте нотатку до колоди
    note_id = add_note_to_deck(note_fields)
    print(f"Нотатка додана з ідентифікатором: {note_id}")
