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
        self.count = 0
        self.filelist = []

    def save(self, parcel='', activity='', msg=''):
        logtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record = {
            'user': self.name,
            'parcel': parcel,
            'activity': activity,
            'msg': msg,
            'logtime': logtime,
        }
        self.collection.insert_one(record)

    def list(self, parcel=''):
        self.filelist = []
        if parcel != '':
            records = self.collection.find({'parcel': {'$eq': parcel}})

            for r in records:
                rec = {'user': r['user'], 'activity': r['activity'], 'msg': r['msg'], 'ts': r['logtime']}
                self.filelist.append(rec)

        # To sort the list in place...
        self.filelist.sort(key=lambda x: x['ts'], reverse=True)

        return self.filelist

