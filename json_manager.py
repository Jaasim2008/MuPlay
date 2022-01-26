import json
from pathlib import Path


class Json_Manager:
    def __init__(self, json_file_name):
        self.json_file_name = json_file_name
        try:
            file = open(self.json_file_name, 'r')
        except Exception as e:
            print(f'(Error Full : "{e}")')

    def write_data(self, key, value):
        try:
            my_dict = {
                key: value
            }
            file = open(self.json_file_name, 'w')
            file.write('')
            data = json.dumps(my_dict, indent=4)
            file.write(data)
            print('Write Data --> Pass')
        except Exception as e:
            print(f'Error : {e}')

    def append_data(self, key, value):
        try:
            my_dict = {
                key: value
            }
            with open(self.json_file_name, 'r+') as file:
                f = Path(self.json_file_name)
                my_data = json.loads(f.read_text())
                my_data[str(key)] = [value]
                f.write_text(json.dumps(my_data, indent=2))
                print('Append Data --> Pass')
        except Exception as e:
            print(f'Error : {e}')

    def clear_data(self):
        try:
            with open(self.json_file_name, 'w') as file:
                file.write('{}')
                print('Clear Data --> Pass')
        except Exception as e:
            print(f'Error : {e}')

    def get_data(self, key):
        try:
            with open(self.json_file_name, 'r') as file:
                data = json.load(file)
                if isinstance(data[key], str):
                    full_data = data[key]
                    print('Got Data --> Pass')
                    return full_data
                elif isinstance(data[key], list):
                    full_data = data[key][0]
                    print('Got Data --> Pass')
                    return full_data
                else:
                    full_data = data[key]
                    print('Got Data --> Pass')
                    return full_data
        except Exception as e:
            print(f'Error : {e}')

    def change_data(self, oldkey, newvalue):
        try:
            with open(self.json_file_name, 'r+') as file:
                f = Path(self.json_file_name)
                my_data = json.loads(f.read_text())
                my_data[str(oldkey)] = newvalue
                f.write_text(json.dumps(my_data, indent=2))
                print('Change Data --> Pass')
        except Exception as e:
            print(f'Error : {e}')
