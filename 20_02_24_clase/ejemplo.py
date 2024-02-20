import json

f = open('../data/users_data_online.json', 'r')
data = json.load(f)
print(data)
print(data['usuarios'])
print(data['usuarios'][0])
print(data['usuarios'][0]['luis.garcia'])


