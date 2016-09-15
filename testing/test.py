import json


with open('data.json') as data_file:
    data = json.load(data_file)

    for post in data:
        data_name = post['name']
        data_type = post['type']
        data_id = post['id']
        data_data = post['data']
        data_props = post['properties']

        print data_id
        print data_name
        print data_type

        for data_item in data_data:
            print data_item

        for prop_item in data_props:
            print prop_item
