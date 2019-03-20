#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 Author: Tlams
 Langage: Python
 Minimum version require: 3.4
"""

from pathlib import Path
from api.v1.api import *
from core.libs.logs import *
import configparser
import getpass
import os
import stat
import urllib3
import argparse


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


if __name__ == "__main__":
    """ Arg parse"""
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    #group.add_argument("-a", "--api", action="store_true",  help="Start only")
    args = parser.parse_args()

    """ Read conf """
    getpathscriptdir = os.path.dirname(sys.argv[0])
    localconf = configparser.ConfigParser()
    localconf.read("private/conf/config")

    generalconf = {
        "logger": {"logs_level": localconf['logger']['logs_level'],
                   "logs_dir": localconf['logger']['logs_dir'], "bulk_write": localconf['logger']['bulk_write'],
                   "bulk_size": localconf['logger']['bulk_size']},

        "mongodb": {"ip": localconf['databases']['mongodb_ip'], 'port': localconf['databases']['mongodb_port']}
    }

    """ Active logger"""
    logger = Logger(generalconf["logger"])
    logger.write({"thread": threading.get_ident(), "result": "INFO", "type": "MAINCORE", "value": "Start logger"})
    logger.write({"thread": threading.get_ident(), "result": "INFO", "type": "MAINCORE", "value": ">>>>>>> -- NEW STARTUP -- <<<<<<<"})

    # URL MAPPING
    urls = \
        (
            # FRESH DATA
            '/api/v1/data/dates', 'Dates',

            '/api/v1/data/', 'Values',
            '/api/v1/data/([0-9]+)/', 'Values',
            '/api/v1/data/([0-9]+)/live', 'Values',

            '/api/v1/config/', 'Manage',
            '/api/v1/config/([0-9]+)', 'Manage',
        )

    """ Init Core thread """
    logger.write({"thread": threading.get_ident(), "result": "INFO", "type": "MAINCORE", "value": "Init Core thread"})
    core = Core(generalconf, logger)

    """ Init API thread """
    logger.write({"thread": threading.get_ident(), "result": "INFO", "type": "MAINCORE", "value": "Init API thread"})
    api_th = ThreadAPI(1, "ThreadAPI", urls, core, generalconf, logger)

    api_th.start()
