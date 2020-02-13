from flask import session, request
from pymongo import MongoClient
import os


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

        uri = 'mongodb://%s:%s' % (os.getenv('SESSION_HOST'), os.getenv('SESSION_PORT'))
        client = MongoClient(uri)
        db = client[os.getenv('SESSION_DB')]
        collection = db['session']

        del_query = {'_id': sess.get('_id')}
        try:
            collection.delete_one(del_query)
        except Exception as e:
            print('Exception: %s' % str(e))