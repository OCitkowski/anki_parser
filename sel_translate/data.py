import logging, json


def get_data_from_json_file(json_file_name):
    words = []
    try:
        with open(json_file_name, 'r') as read_file:
            template = json.load(read_file)
            logging.info(f"{json_file_name}.json get data from json file")
            words = ((note['fields'][0], note['fields'][8], note['fields'][9], note['fields'][10]) for note in
                     template['notes'] if note['fields'][8] != '')
    except Exception as e:
        logging.info(f"{json_file_name}.json don`t get data from json file || {e}")
    print(words)
    return words


def in_der_die_das(words: list):
    der_die_das = ['der', 'die', 'das']

    if len(words) > 1 and words[0] in der_die_das:
        word = words[1]
    else:
        word = words[0]

    return word


def save_data_in_json_file(data, json_file_name):
    result = False
    try:
        with open(json_file_name, 'w') as write_file:
            json.dump(data, write_file, ensure_ascii=False)
            result = True
        print(f'{json_file_name}.json save to root')
    except:
        print(f'{json_file_name}.json don`t save to root')
    return result



def update_row_in_json_file(id, row, json_file_name):
    # Відкрити файл xxx.json і зчитати дані в об'єкт Python
    with open(json_file_name) as f:
        data = json.load(f)

    # Знайти стрічку, яку потрібно змінити, і замінити на нову
    data[id][1] = row
    data[id][4] = True

    # Зберегти зміни в файл
    with open(json_file_name, 'w') as f:
        json.dump(data, f)


def get_data_from_json_file2(json_file_name):
    try:
        with open(json_file_name, 'r') as read_file:
            template = json.load(read_file)
            logging.info(f"{json_file_name}.json get data from json file")
            # words = (i for i in template)
            # print(template)
    except:
        logging.info(f"{json_file_name}.json don`t get data from json file")

    return template



def get_proxies_txt(filename):
    with open(filename + '.txt', 'r') as f:

        lines = f.readlines()
        # Відфільтровуємо перший рядок, який містить назву та дату
        lines = [line.strip() for line in lines if 'Free proxies' not in line and 'Updated' not in line]
        # Перетворюємо решту рядків з файлу на список проксі
        proxies = [line.strip() for line in lines if line.strip()]
    print(proxies)




if __name__ == '__main__':
    logging.basicConfig(filename='DEBUG.log', encoding='utf-8', level=logging.DEBUG)
    # json_file_name = 'deck.json'
    # data = {}
    # for i, j in enumerate(get_data_from_json_file(json_file_name)):
    #     if len(j[0].split(' ')) < 3:
    #         # print(i, j, len(j[0].split(' ')), in_der_die_das(j[0].split(' ')))
    #         data[j[3]] = [in_der_die_das(j[0].split(' ')), '*****', j[1], i, False]
    # #
    # # for x, y in data.items():
    # #     print(x, y)
    #
    # save_data_in_json_file(data, json_file_name='data.json')
    #
    # data = get_data_from_json_file2(json_file_name='data.json')
    #
    # for x, y in data.items():
    #     print(x, y)
    # row = [1, 'iuuiz', 987987]
    # id = "23493977"
    # update_row_in_json_file(id, row, 'data.json')

    get_proxies_txt('free_proxy')
