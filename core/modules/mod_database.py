from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
import json
import redis
import time

class Redis_wrapper:
    def __init__(self, server="127.0.0.1", port=6379, db=0, password=None):
        # DB =
        # messages: 0
        # logs: 1
        # queue : 2
        # cache : 3

        self.server = server
        self.port = port
        self.r = None
        self.db = db
        self.password = password

    def connect(self):
        try:
            conn = self.r = redis.StrictRedis(
                host=self.server, port=self.port, db=self.db, password=self.password,
                charset="utf-8", decode_responses=True)
            self.r.client_list()
            return conn
        except BaseException as err:
            print("Redis connexion error on {0}:{1} ({2})".format(self.server, self.port, err))

    def insert_instances_queue(self,  logtext, expir=3000):
        self.r.set(time.time(), logtext, expir)

    def insert_logs(self,  logtext, expir=86400*4):
        self.r.set(time.time(), logtext, expir)

    def insert_message(self, key, value, expir=86400):
        self.r.set(key, value, expir)

    def get_message(self, key):
        try:
            result = json.loads(dumps(self.r.get(key)))
        except BaseException as e:
            result = {
                "result": "ERROR",
                "type": "Redis - Request on get_message",
                "value": "Invalid request: {0}".format(e)
            }
        return result

class MongoDB:
    def __init__(self, server="127.0.0.1", port=27017):
        """
        :param server:
        :param port:
        """
        self.server = server
        self.port = port
        self.collection_system = "system"
        self.port = port
        self.db = None
        self.client = None


    def __mappingcol(self, col):
        if col == "system":
            collection = self.collection_system
        else:
            collection = ""
        return collection

    def connect(self):
        try:
            conn = MongoClient(self.server + ':' + str(self.port))
            conn.server_info()
            return conn
        except BaseException as err:
            print("MongoDB connexion error on {0}:{1} ({2})".format(self.server, self.port, err))

    def authenticate(self, user=None, password=None, mechanism='SCRAM-SHA-1'):
        try:
            self.client.db.authenticate(user, password, mechanism)
        except (TypeError, ValueError) as e:
            print("MongoDB authentification error on {0}:{1} ({2})".format(self.server, self.port, e))

    def generalmongosearch(self, collection, id):
        try:
            result = {
                "result": "OK",
                "value": json.loads(dumps(self.db[collection].find_one({"_id": ObjectId(id)})))
            }
        except BaseException as e:
            result = {
                "result": "ERROR",
                "type": "MongoDB - Request on generalmongosearch",
                "value": "Invalid request: {0}".format(e)
            }
        return result

    def get_system_info(self):
        return self.db[self.collection_system].find_one({"_id": "0"})

    def update_system_instances_id(self, value):
        self.db[self.collection_system].update({'_id': "0"}, {'$set': {'instances_number': value}})

    def update_system_instances_ip(self, value):
        self.db[self.collection_system].update({'_id': "0"}, {'$set': {'IP_current': value}})

    def update_system_free_ip(self, value):
        self.db[self.collection_system].update({'_id': "0"}, {'$push': {'IP_free': value}}, upsert=False)

    def update_system_delete_ip(self, value):
        self.db[self.collection_system].update({'_id': "0"}, {'$pull': {'IP_free': value}}, upsert=False)
