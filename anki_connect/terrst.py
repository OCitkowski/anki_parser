import os
import requests
import re
from anki_utils import invoke, get_notes_info

deck_name = 'Satze'
model_name = 'Satze'  # Вкажіть модель, яку ви використовуєте в Anki
output_directory = 'audio_files'  # Папка, де зберігатимуться аудіофайли


def retrieve_audio_file(url, output_filename):
    audio_data = requests.get(url).content
    if audio_data:
        with open(output_filename, 'wb') as audio_file:
            audio_file.write(audio_data)
        print(f"Аудіофайл {output_filename} отримано та збережено на диск.")
    else:
        print(f"Не вдалося отримати аудіофайл {output_filename}.")


def get_audio_files():
    os.makedirs(output_directory, exist_ok=True)
    notes = get_notes_info(deck_name)
    print('***')

    for note_id in notes:
        print('***')
        note = invoke('notesInfo', notes=[note_id])[0]
        fields = note['fields']
        for field_name, field_content in fields.items():
            if field_name in ['SD', 'SU']:
                print(field_name, field_content['value'])
                audio_urls = re.findall(r'\[sound:(.*?)\]', field_content['value'])
                for audio_url in audio_urls:
                    output_filename = os.path.join(output_directory, os.path.basename(audio_url))
                    retrieve_audio_file(audio_url, output_filename)


if __name__ == '__main__':
    get_audio_files()
