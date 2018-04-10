import json

with open('data.json','r') as f:
    t_dict = json.load(f)

string = ''
print(t_dict)
for name in t_dict:
    if name == 'image_index':
        string += str(t_dict[name])
        string += ' '
    if name == 'question':
        string += str(t_dict[name])


print(string)
