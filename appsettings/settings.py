import copy
import json
import base64
from .encdec import EncDec


class Defaults:

    def __init__(self):
        self.appname = 'parceldocs'
        self.values = [
            {'name': 'appname', 'value': 'parceldocs', 'type': 'text'},
            {'name': 'mongo_host', 'value': 'localhost', 'type': 'text'},
            {'name': 'mongo_port', 'value': '27017', 'type': 'text'},
            {'name': 'mongo_db', 'value': 'parceldocs', 'type': 'text'},
            {'name': 'session_cookie', 'value': 'pdcookie', 'type': 'text'},
            {'name': 'sqlserver', 'value': 'sql-svr\\mssqlr2', 'type': 'text'},
            {'name': 'sqldb', 'value': 'wmis_ibm', 'type': 'text'},
            {'name': 'sql-trusted', 'value': 'y', 'type': 'text'},
            {'name': 'sql-user', 'value': '', 'type': 'text'},
            {'name': 'sql-password', 'value': '', 'type': 'password'},

            {'name': 'root_folder', 'value': 'd:\\parcel_docs', 'type': 'text'},
            {'name': 'ad_api', 'value': 'https://host.com', 'type': 'text'},
            {'name': 'ad_api_key', 'value': 'secret-key', 'type': 'password'},

            {'name': 'ms-client_secret', 'value': 'value', 'type': 'password'},
            {'name': 'ms-authority', 'value': 'value', 'type': 'text'},
            {'name': 'ms-client_id', 'value': 'value', 'type': 'text'},
            {'name': 'ms-redirect_path', 'value': 'value', 'type': 'text'},
            {'name': 'ms-scope', 'value': 'value', 'type': 'text'},

            {'name': 'session_host', 'value': 'localhost', 'type': 'text'},
            {'name': 'session_port', 'value': '27017', 'type': 'text'},
            {'name': 'session_db', 'value': 'session', 'type': 'text'},

            {'name': 'host-url', 'value': 'http://localhost:5000', 'type': 'text'},
        ]
        return

    def get(self, name):
        result = ''
        try:
            for v in self.values:
                if v['name'].lower() == name.lower():
                    result = v['value']
                    break
        except KeyError as e:
            result = str(e)
        return result

    def get_type(self, name):
        result = ''
        try:
            for v in self.values:
                if v['name'].lower() == name.lower():
                    if 'type' in v:
                        result = v['type']
                    break
        except KeyError as e:
            result = str(e)
        return result


class Settings:

    def __init__(self):
        import copy
        defaults = Defaults()
        # make a non-referenced copy of the defaults.
        self.items = []
        self.load_config()

    def config_filename(self):
        import os
        osname = os.name
        if osname == 'nt':
            _data_folder = os.path.join(os.getenv('APPDATA'), Defaults().appname)
        else:
            _data_folder = os.path.join(os.getenv('HOME'), Defaults().appname)

        if not os.path.exists(_data_folder):
            os.makedirs(_data_folder)

        filename = os.path.join(_data_folder, 'settings')
        return filename

    def load_config(self):
        filename = self.config_filename()
        try:
            with open(filename, 'r') as f:
                _enc_ = f.read()
                _text_ = EncDec().decrypt(_enc_)
                self.items = json.loads(_text_)
        except FileNotFoundError:
            self.items = copy.deepcopy(Defaults().values)
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
                new_item = {'name': i['name'], 'value': i['value'], 'type': i['type']}
                self.items.append(new_item)
        #
        # Add types to each item where missing.
        #
        for item in self.items:
            item['type'] = Defaults().get_type(item['name'])


    def save_config(self):
        filename = self.config_filename()
        try:
            with open(filename, 'w') as output_file:
                _text_ = json.dumps(self.items)
                _enc_ = EncDec().encrypt(_text_)
                output_file.write(_enc_)
        except Exception as e:
            print(str(e))


    def get(self, name: str = ''):
        result = ''
        for item in self.items:
            if name == item['name']:
                result = item['value']
                break
        return result

    def get_type(self, name: str = ''):
        result = ''
        for item in self.items:
            if name == item['name']:
                if 'type' in item:
                    result = item['type']
                else:
                    result = ''
                break
        return result


    def set(self, name: str = '', value: str = '', type: str = ''):
        item_found = False
        for item in self.items:
            if name == item['name']:
                item['value'] = value
                item['type'] = type
                item_found = True
                break
        if not item_found:
            item = { 'name': name, 'value': value, 'type': type }
            self.items.append(item)

        return

    def __str__(self):
        return json.dumps(self.items)


