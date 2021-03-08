"""
Auxiliary library for methods used in testcases
"""
import os
import requests
import json
import urllib
from libs import builtins, consts
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import xml.etree.ElementTree as ET

CURRENT_PAGE = None
FILE_LOG ="API_logs_%s.txt" %time.strftime('%Y%m%d_%H%M%S')
"""
"""
from datetime import datetime

# Clean log on import
with open(os.path.join(builtins.PROJECT_PATH, "reports", FILE_LOG), "w") as wh:
    pass

def log(msg):
    with open(os.path.join(builtins.PROJECT_PATH, "reports", FILE_LOG), "a") as ah:
        ah.write(msg)
        ah.write("\n")

def log_request(func, *args, **kwargs):
    def aux(*args, **kwargs):
        log("REQUEST: {} - {}".format(args, kwargs))
        result = func(*args, **kwargs)
        log(" > RESPONSE: {}".format(result))
        return result

    return aux

def log_test(func, *args, **kwargs):
    def aux(*args, **kwargs):
        log("\n--- TEST: {}  ({}) ---".format(func.__name__, str(datetime.now())))
        result = func(*args, **kwargs)
        log("--- END ({}) ---\n\n".format(str(datetime.now())))
        return result

    return aux

@log_request
def send_request(url, data, **params):
    """
        Auxiliary method to send Request
    """
    if params['request_type'] == "POST":
        response = requests.post(builtins.API_URL + url + "?" + urllib.parse.urlencode(params),
            data = data)
    elif params['request_type'] == "GET":
        response = requests.get(builtins.API_URL + url + "?" + urllib.parse.urlencode(params))
    else:
        raise ValueError("Request Type is not supported")

    # Format the response into JSON if possible
    if response.headers['Content-Type'] == 'application/json;charset=utf-8':
        return json.loads(response.text)

    """    
    elif response.headers['Content-Type'] == 'application/xml;charset=utf-8':
        return ET.fromstring(response.text)
    """

    return response

def send_get_request(url, **params):
    """
        Auxiliary method to load API TOKEN together with uri params to symplify testcase syntax
    """
    if 'api_key' not in params.keys():
        params['api_key'] = builtins.API_KEY
    params['request_type'] = "GET"
    if "data" in params.keys():
        return send_request(url, **params)
    else:
        return send_request(url, data="", **params)

def send_post_request(url, data, **params):
    """
        Auxiliary method to load API TOKEN together with uri params to symplify testcase syntax
    """
    params['api_key']= builtins.API_KEY
    params['request_type']= "POST"
    return send_request(url, data, **params)

def wait_for_page_to_load(tries=10, interval=0.2):
    """ Waits for the page to load"""
    time.sleep(0.5)
    for _ in range(tries):
        if builtins.DRIVER.execute_script('return document.readyState;') != 'complete':
            time.sleep(interval)
        else:
            break
    else:
        raise ValueError("URL failed to load in the given time")

def find_current_page():
    global CURRENT_PAGE
    CURRENT_PAGE = None
    for p in builtins.PO:
        CURRENT_PAGE = builtins.PO[p] if builtins.DRIVER.current_url == builtins.BASE_URL + builtins.PO[p]["PATH"] else False
        if CURRENT_PAGE:
            break

def find_po_element_by_alias(element):
    for alias in CURRENT_PAGE["ELEMENTS"]:
        if alias == element:
            return CURRENT_PAGE["ELEMENTS"][alias]

def find_element(element, wait_for_element= True):
    """ finds an element of idtype with value id """
    find_current_page()
    try:
        assert CURRENT_PAGE
    except:
        raise ValueError("\"{}\" page wasn't found within PO".format(builtins.DRIVER.current_url))

    el = find_po_element_by_alias(element)

    if wait_for_element:
        timer = int(wait_for_element) if type(wait_for_element) != bool else 10
        try:
            WebDriverWait(builtins.DRIVER, timer).until(EC.presence_of_element_located((consts.SEARCH_BY_TYPES[el['type']],el['locator'])))
        except TimeoutException:
            raise ValueError("Could not wait for element [{}]{}".format(consts.SEARCH_BY_TYPES[el['type']],el['locator']))
    search_function = 'builtins.DRIVER.{}("{}")'.format(consts.SEARCH_TYPES[el['type']], el['locator'])
    return eval(search_function)

def wait_for_element_to_be_present(element,wait_for_element=10):
    find_current_page()
    try:
        assert CURRENT_PAGE
    except:
        raise ValueError("\"{}\" page wasn't found within PO".format(builtins.DRIVER.current_url))

    el = find_po_element_by_alias(element)
    timer = int(wait_for_element) if type(wait_for_element) != bool else 10
    try:
        WebDriverWait(builtins.DRIVER, timer).until(
            EC.presence_of_element_located((consts.SEARCH_BY_TYPES[el['type']], el['locator'])))
    except TimeoutException:
        raise ValueError("Could not wait for element [{}]{}".format(consts.SEARCH_BY_TYPES[el['type']], el['locator']))

def i_fill_in_the_object_with_text(element, text):
    """
        Finds and fills up the object with the given text:
    """
    find_element(element).send_keys(text)

def i_clear_the_object(element):
    """
        Finds and clear the object value:
    """
    find_element(element).clear()

def i_click_the_object(element):
    """
     Finds and clicks the button/object:
    """
    find_element(element).click()
    time.sleep(0.5)

def current_page_is(page):
    """
     Finds and clicks the button/object:
    """
    find_current_page()
    try:
        assert CURRENT_PAGE["PATH"] == builtins.PO[page]["PATH"]
    except:
        raise ValueError("Current page is not \"{}\", current page is \"{}\"".format(page, CURRENT_PAGE['ALIAS']))

