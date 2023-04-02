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