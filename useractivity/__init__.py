from flask import session, request, g
from pymongo import MongoClient
from appsettings import Settings
import datetime


class UserActivity:

    def __init__(self):
        self.name = g.auth['name']
        settings = Settings()
        uri = 'mongodb://%s:%s' % (settings.get('session_host'), settings.get('session_port'))
        self.client = MongoClient(uri)
        self.db = self.client[settings.get('session_db')]
        self.collection = self.db['log']

    def save(self, parcel='', activity='', msg=''):
        logtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        id = parcel + ':' + logtime
        record = {
            '_id': id,
            'user': self.name,
            'parcel': parcel,
            'activity': activity,
            'msg': msg,
            'logtime': logtime,
        }
        self.collection.insert_one(record)

    def list(self, parcel=''):
        pass

