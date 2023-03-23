import json

if __name__ == '__main__':
    # Opening JSON file
    f = open('deck.json')
    # returns JSON object as
    # a dictionary
    data = json.load(f)

    # Iterating through the json
    # list
    for i in data['notes']:
        # print(type(i))
        # print(i['fields'])
        print(f" {i['fields'][0]} ///  {i['fields'][3] } ")
        # for j in i['fields']:
        #     print(j[0])


    # Closing file
    f.close()
