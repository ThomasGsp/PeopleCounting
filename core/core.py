#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 Author: Tlams
 Langage: Python
 Minimum version require: 3.4
"""

from core.modules.counter.people_counter import *
from core.modules.mod_database import *
import threading
import time
import base64
import hashlib
import pymongo


def Runthcam(generalconf, logger, CAM):
    play = RunAnalyseCam(generalconf, logger, CAM)
    play.run()



class Core:
    def __init__(self, generalconf, logger):


        self.generalconf = generalconf
        self.logger = logger
        self.logger.write({"thread":threading.get_ident() ,"result": "INFO", "type": "MAINCORE",
                           "value": "Start Core process"})

        """ LOAD MONGODB """
        self.logger.write({"thread": threading.get_ident(), "result": "INFO", "type": "MAINCORE",
                           "value": "MongoDB connection"})
        self.mongo = MongoDB(generalconf["mongodb"]["ip"])
        self.mongo.client = self.mongo.connect()


        if self.mongo.client:
            self.mongo.db = self.mongo.client.db

            """ Create indexes"""
            #self.setupindexes()

            """ RUN THE ANALYZER IN DEDICATED THEARD"""
            """ Clean previous lockers """
            self.logger.write({"thread": threading.get_ident(), "result": "INFO", "type": "MAINCORE",
                               "value": "Clean Locker"})


            HttpCam = [
                {'name': "MyCam01", "httpstream": "129.2.2.2"},
            ]

            for CAM in HttpCam:
                threading.Thread(name="Start CAM {0}".format(CAM['name']),
                                       target=Runthcam,
                                       args=(self.generalconf, self.logger, CAM)).start()


        else:
            exit(1)


def setupindexes(self):
    self.mongo.set_indexes("data",
                           [('date', pymongo.ASCENDING), ("cluster", pymongo.ASCENDING),
                            ("node", pymongo.ASCENDING), ("vmid", pymongo.ASCENDING)])
    indexes_result = {
        "value": "{0}".format("All indexes created"),
        "result": "OK",
        "type": "MAINCORE"
    }

    return indexes_result