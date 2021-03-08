"""'this file contains methods to initialize the test variables into builtins'

import json
import os
from libs.driver import *
from libs import builtins

#####################################################################################################
with open(os.path.join(os.path.abspath(os.getcwd()), 'config.json'),'r') as fc:
    data = json.load(fc)
    builtins.BROWSER = data["BROWSER"]
    builtins.ENV = data["ENV"]
    builtins.BASE_URL = data["URL_FOR_ENV"][builtins.ENV]
    builtins.API_URL = data["API_URL"]
    builtins.API_KEY = data["TOKEN"]

#####################################################################################################
"""
#innit global driver and make it accessible from builtins
"""

def init_driver():
    if builtins.BROWSER == 'chrome':
        builtins.DRIVER = chrome().driver
"""
