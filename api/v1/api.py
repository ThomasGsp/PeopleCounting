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

    def GET(self, camid=""):
        try:
            if camid:
                result = core.list_cam(camid)
            else:
                result = core.list_cam()

        except BaseException as e:
            result = {
                "result": "ERROR",
                "type": "API",
                "value": "Invalid request: {0}".format(e)
            }
        return result

    def POST(self):
        try:
            data = json.loads(web.data().decode('utf-8'))
            if data['httpstream'] and data['name']:
                data["camid"] = random.randint(99999, 99999999)
                result = core.insert_cam(data)
            else:
                result = {
                    "result": "ERROR",
                    "type": "API",
                    "value": "Invalid request: Name and/or httpstream not found"
                }
        except BaseException as e:
            result = {
                "result": "ERROR",
                "type": "API",
                "value": "Invalid request: {0}".format(e)
            }
        return result

    def DELETE(self, camid=""):
        try:
            if camid:
                result = core.del_cam(camid)
            else:
                result = {
                    "result": "ERROR",
                    "type": "API",
                    "value": "Invalid request: Name and/or id not found"
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
    def GET(self, camid, rq):
        try:
            if camid:
                if rq == "live":
                    result = core.get_count(camid, "live")
                else:
                    result = core.get_count(camid)
            else:
                result = {
                    "result": "ERROR",
                    "type": "API",
                    "value": "no cam id found: {0}".format(core.list_cam())
                }

        except BaseException as e:
            result = {
                "result": "ERROR",
                "type": "API",
                "value": "(bc) Invalid request: {0}".format(e)
            }
        return result

    def POST(self):
        try:
            data = json.loads(web.data().decode('utf-8'))
            if data['camid']:
                result = core.insert_count(data)
            else:
                result = {
                    "result": "ERROR",
                    "type": "API",
                    "value": "Invalid request: Name and/or httpstream not found"
                }
        except BaseException as e:
            result = {
                "result": "ERROR",
                "type": "API",
                "value": "Invalid request: {0}".format(e)
            }
        return result

class ThreadAPI(threading.Thread):
    #def __init__(self, threadid, name, urls, c, g, r):
    def __init__(self, threadid, name, urls, c, g, logger):
        """ Pass Global var in this theard."""
        global core, generalconf
        core = c
        generalconf = g

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
