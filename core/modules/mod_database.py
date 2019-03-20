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
        self.col_cam = "cam"
        self.col_counter = "counter"
        self.port = port
        self.db = None
        self.client = None


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

    def insert_cam(self, data):
        return self.db[self.col_cam].insert({'camid': data["camid"], 'name': data["name"], 'httpstream': data["httpstream"]})

    def del_cam(self, camid):
        pass

    def list_cam(self, camid=""):
        if camid:
            return self.db[self.col_cam].find({'camid': camid})
        else:
            return self.db[self.col_cam].find().sort("camid", -1)

    def insert_count(self, data):
        return self.db[self.col_counter].insert({'camid': data["camid"], 'up': data["up"], 'down': data["down"], 'status': data["status"]})

    def get_count(self, camid, rq=None):
        if rq == "live":
            return self.db[self.col_counter].find_one({'camid': camid}).sort("camid", -1)
        else:
            return self.db[self.col_counter].find({'camid': camid}).sort("camid", -1)
        pass


