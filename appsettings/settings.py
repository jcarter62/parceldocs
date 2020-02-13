import copy
import json


class Defaults:

    def __init__(self):
        self.values = [
            {'name': 'appname', 'value': 'parceldocs'},
            {'name': 'mongo_host', 'value': 'localhost'},
            {'name': 'mongo_port', 'value': '27017'},
            {'name': 'mongo_db', 'value': 'parceldocs'},
            {'name': 'session_cookie', 'value': 'pdcookie'},
            {'name': 'sqlserver', 'value': 'sql-svr\\mssqlr2'},
            {'name': 'sqldb', 'value': 'wmis_ibm'},
            {'name': 'root_folder', 'value': 'd:\\parcel_docs'},
            {'name': 'ad_api', 'value': 'https://host.com'},
            {'name': 'ad_api_key', 'value': 'secret-key'},

            {'name': 'ms-client_secret', 'value': 'value'},
            {'name': 'ms-authority', 'value': 'value'},
            {'name': 'ms-client_id', 'value': 'value'},
            {'name': 'ms-redirect_path', 'value': 'value'},
            {'name': 'ms-scope', 'value': 'value'},

        ]
        return

    def get(self, name):
        result = ''
        try:
            for v in self.values:
                if v['name'] == name:
                    result = v['value']
                    break
        except KeyError as e:
            result = str(e)

        return result


class Settings:

    def __init__(self):
        import copy
        defaults = Defaults()
        # make a non-referenced copy of the defaults.
        self.items = copy.deepcopy(defaults.values)
        self.load_config()

    def config_filename(self):
        import os
        osname = os.name
        if osname == 'nt':
            _data_folder = os.path.join(os.getenv('APPDATA'), self.get('appname'))
        else:
            _data_folder = os.path.join(os.getenv('HOME'), self.get('appname'))

        if not os.path.exists(_data_folder):
            os.makedirs(_data_folder)

        filename = os.path.join(_data_folder, 'settings.json')
        return filename

    def load_config(self):
        filename = self.config_filename()
        try:
            with open(filename, 'r') as f:
                self.items = json.load(f)
        except OSError as e:
            print(str(e))
        #
        # add any missing items
        #
        for i in Defaults().values:
            def_name = i['name']
            found = False
            for item in self.items:
                if item['name'] == def_name:
                    found = True
                    break
            if not found:
                new_item = {'name': i['name'], 'value': i['value']}
                self.items.append(new_item)
        # completed with adding missing items.

    def save_config(self):
        filename = self.config_filename()
        try:
            with open(filename, 'w') as output_file:
                json.dump(self.items, output_file)
        except Exception as e:
            print(str(e))

    def get(self, name: str = ''):
        result = ''
        for item in self.items:
            if name == item['name']:
                result = item['value']
                break
        return result

    def set(self, name: str = '', value: str = ''):
        item_found = False
        for item in self.items:
            if name == item['name']:
                item['value'] = value
                item_found = True
                break
        if not item_found:
            item = { 'name': name, 'value': value }
            self.items.append(item)

        return

    def __str__(self):
        return json.dumps(self.items)


