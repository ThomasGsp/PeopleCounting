#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import web
from core.core import *
import json
import time
import random
import ast


class Manage:
    def POST(self, data):
        try:
            data = json.loads(web.data().decode('utf-8'))
            """ Overwrite name """
            if data['api_pwd'] == "sfgf5saGFDF4eFS":
                data["camid"] = random.randint(99999,99999999)
                result = core.insert_cam(data)
            else:
                result = {
                    "result": "ERROR",
                    "type": "API",
                    "value": "Invalid password"
                }

        except BaseException as e:
            result = {
                "result": "ERROR",
                "type": "API",
                "value": "Invalid request: {0}".format(e)
            }
        return result

    def DELETE(self, data):
        try:
            data = json.loads(web.data().decode('utf-8'))
            """ Overwrite name """
            if data['api_pwd'] == "sfgf5saGFDF4eFS":
                result = core.del_cam(data)
            else:
                result = {
                    "result": "ERROR",
                    "type": "API",
                    "value": "Invalid password"
                }
        except BaseException as e:
            result = {
                "result": "ERROR",
                "type": "API",
                "value": "Invalid request: {0}".format(e)
            }
            return result

class Dates:
    def GET(self, keytype):
        try:
            result = core.getkey(keytype)
        except BaseException as e:
            result = {
                "result": "ERROR",
                "type": "API",
                "value": "Invalid request: {0}".format(e)
            }
        return json.dumps(result)


class Values:
    def GET(self, rq):
        try:
            if rq == "live":
                result = core.getlive()["value"]
            else:
                result = core.getlive(rq)["value"]

        except BaseException as e:
            result = {
                "result": "ERROR",
                "type": "API",
                "value": "(bc) Invalid request: {0}".format(e)
            }
        return result


class ThreadAPI(threading.Thread):
    #def __init__(self, threadid, name, urls, c, g, r):
    def __init__(self, threadid, name, urls, c, g, logger):
        """ Pass Global var in this theard."""
        global core, generalconf, redis_msg
        core = c
        generalconf = g
        redis_msg = core.redis_msg

        """ RUN API """
        threading.Thread.__init__(self)
        self.threadID = threadid
        self.threadName = name
        self.app = HttpApi(urls, globals())
        self.app.notfound = notfound

    def run(self):
        print("Start API server...")
        self.app.run()

    def stop(self):
        print("Stop API server...")
        self.app.stop()


def notfound():
    return web.notfound({"value": "Bad request"})

class HttpApi(web.application):
    def run(self, ip="127.0.0.1", port=8080, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, (ip, int(port)))
