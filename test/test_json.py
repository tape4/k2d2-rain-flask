import json

file_path = '/home/ubuntu/rain_api/result/gis_points_coordinates.json'

with open(file_path, 'r', encoding='utf-8') as file:
    python_dict = json.load(file)
print(python_dict)

for i in range(100):
    for j in range(100):
        if ({'row': i, 'col': j} in python_dict):
            print(i, j)
    