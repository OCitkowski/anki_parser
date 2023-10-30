# https://github.com/FooSoft/anki-connect
# /home/fox/.config/google-chrome/Default
from anki_utils import invoke, add_note_to_deck

deck_name = 'Satze'
modelName = 'Satze'  # Вкажіть модель, яку ви використовуєте в Anki

if __name__ == '__main__':
    # Ваша колода та дані для нотатки

    note_fields = {
        'Deutsch': 'значення16r2',
        'Ukr': 'значення2362'
        # Додайте інші поля та значення, які вам потрібні
    }

    # Ваш файл і нотатки
    with open('Test.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        deutsch, ukr = [part.strip() for part in line.split('/')]
        note_id = add_note_to_deck(deutsch, ukr, deck_name, modelName)
        print(f"Нотатка додана з ідентифікатором: {note_id}")
