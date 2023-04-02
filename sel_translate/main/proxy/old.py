# if path.isfile(DataFile):
#     file_with_data = open(DataFile, "rt")
#     words_count_sort = fill_words_count_from_file(file_with_data, lower_word=False)
#
#     path_to_file_result = OutputFile
#
#     save_data_to_file(words_count_sort, path_to_file_result, div)
#
#     file_with_data.close()
#     print(f'Ok')
# else:
#     print(f'file not exist')

# while True:
#     # отримуємо перший елемент зі списку та видаляємо його
#     proxy = r.lpop('proxies')
#     # print(proxy)
#     if proxy is None:
#         break
#     print(proxy.decode())
# sudo chmod 777 sel_translate/main/proxy/proxy.log

import logging, datetime

if __name__ == '__main__':
    logging.basicConfig(
        filename='proxy.log',
        encoding='utf-8',
        datefmt='%Y-%m-%d_%H-%M-%S',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filemode='a'  # додати записи до файлу з логами, якщо він вже існує
    )
    logging.info(f"{datetime.datetime.now()} // Is working!")