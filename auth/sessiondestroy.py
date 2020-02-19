from flask import session, request
from pymongo import MongoClient
import os
from appsettings import Settings


class SessionDestroy:

    def __init__(self, sess: session = None, req: request = None):

        if (sess is None) or (req is None):
            return

        skeys = []
        for s in session.keys():
            if s[0:1] != '_':
                skeys.append(s)

        for key in skeys:
            session.pop(key)

        settings = Settings()

        uri = 'mongodb://%s:%s' % (settings.get('session_host'), settings.get('session_port'))
        client = MongoClient(uri)
        db = client[settings.get('session_db')]
        collection = db['session']

        del_query = {'_id': {'$eq': sess.get('_id')}}
        try:
            collection.find_one_and_delete(del_query)
        except Exception as e:
            print('Exception: %s' % str(e))