import json
import os

PROJECT_PATH = os.path.abspath(os.getcwd())
BROWSER = None
DRIVER = None
ENV = None
BASE_URL = None
PO = None
API_URL = None
API_KEY = None
URL_FOR_ENV = None
VERBOSITY_LEVEL = 2
RECURSIVE = True
VIRTUAL_DISPLAY = None
HEADLESS = None
BROWSER_WIDTH = None
BROWSER_HEIGHT = None

def prepare_results():
    # When a project is started from scratch these folders do not exist; added validation to create them if needed
    if not os.path.exists(os.path.join(PROJECT_PATH, "reports")):
        os.mkdir(os.path.join(PROJECT_PATH, "reports"))
    if not os.path.exists(os.path.join(PROJECT_PATH, "reports", "history")):
        os.mkdir(os.path.join(PROJECT_PATH, "reports", "history"))
    import shutil
    import glob
    try:
        for filename in glob.glob(os.path.join(PROJECT_PATH, "reports", "*.*")):
            shutil.move(filename, (os.path.join(PROJECT_PATH, "reports", "history")))
    except Exception as e:
       import re
       if re.search("Destination path '([^\"]*)' already exists", str(e.args)):
            pass