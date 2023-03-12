# for usage enter in terminal  & python main.py --input 'data.txt' --output 'new.txt'


from os import path
import argparse


def fill_words_count_from_file(file_with_data, lower_word=False):
    words_count = {}

    for line in file_with_data:

        words = set(line.split())
        for word in words:

            word = word.translate({ord(i): None for i in '‚‘«»123“,.„–"[]?()!<>~@#$%^&*()_+=-1234567890;:…'})
            if lower_word:
                word = word.lower()

            word = word.replace("'", '')
            if 'http//' in word:
                continue
            if word in words_count.keys():
                words_count[word] += 1
            else:
                words_count[word] = 1
    words_count_sort = dict(sorted(words_count.items(), key=lambda item: item[1], reverse=True))
    return words_count_sort


def save_data_to_file(data, path_to_file_result):
    # "OutputFile.txt"
    if path_to_file_result == None:
        path_to_file_result = "OutputFile.txt"

    if path.isfile(path_to_file_result):
        result_f = open(path_to_file_result, "wt")
    else:
        result_f = open(path_to_file_result, "at")

    text = ''
    for i, j in data.items():
        text += f'{i} -- {j}  \n'

    result_f.write(text)
    result_f.close()


if __name__ == '__main__':
    descStr = "Python counter words in file txt . For usage enter in terminal  " \
              "& python3 main.py -in_file 'Test_german.txt' -out_file 'new.txt'"
    parser = argparse.ArgumentParser(description=descStr)
    parser.add_argument('-in_file', dest='DataFile', required=True)
    parser.add_argument('-out_file', dest='OutputFile', required=False)
    args = parser.parse_args()
    DataFile = args.DataFile
    OutputFile = args.OutputFile

    if path.isfile(DataFile):
        file_with_data = open(DataFile, "rt")
        words_count_sort = fill_words_count_from_file(file_with_data, lower_word=False)

        path_to_file_result = OutputFile

        save_data_to_file(words_count_sort, path_to_file_result)

        file_with_data.close()
        print(f'Ok')
    else:
        print(f'file not exist')
