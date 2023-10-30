import os
import re
from anki_utils import invoke, get_notes_info, retrieve_audio_file

deck_name = 'Satze'
model_name = 'Satze'  # Вкажіть модель, яку ви використовуєте в Anki
output_directory = 'audio_files'  # Папка, де зберігатимуться аудіофайли


def retrieve_audio_file():
    filename = 'sound:google-85d48e18-99878f31-b3944b13-31678411-6325f384.mp3'
    audio_data = invoke('retrieveMedia', filename=filename)
    if audio_data:
        with open(filename, 'wb') as audio_file:
            audio_file.write(audio_data)
        print(f"Аудіофайл {filename} отримано та збережено на диск.")
    else:
        print(f"Не вдалося отримати аудіофайл {filename}.")


def get_audio_files():
    # Створіть папку для зберігання аудіофайлів, якщо вона не існує
    os.makedirs(output_directory, exist_ok=True)

    # Отримайте всі нотатки з вказаною колодою і моделлю
    notes = get_notes_info(deck_name)

    # Пройдіться по кожній нотатці та знайдіть аудіофайли в полях
    for note_id in notes:
        note = invoke('notesInfo', notes=[note_id])[0]
        fields = note['fields']
        for field_name, field_content in fields.items():
            if field_name in ['SD', 'SU']:
                print(field_name, field_content['value'])
                retrieve_audio_file(field_content['value'])


if __name__ == '__main__':
    retrieve_audio_file()

    # get_audio_files()
