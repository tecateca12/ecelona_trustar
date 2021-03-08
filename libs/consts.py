# -*- coding=utf-8 -*-
from selenium.webdriver.common.by import By


# All valid selector types
SEARCH_TYPES = {
    "": None, # Used for PO                         # empty string defaults to PO
    "id": "find_element_by_id",                     # "id": find by id
    "x":  "find_element_by_xpath",                  # "n": find by name
    "n":  "find_element_by_name",                   # "x": find by xpath
    "pn": None,                                     # Finds element by partial name
    "t": None,                                      # Finds element by its containing text
    "et": None,                                     # Finds element by its equal text.
    "lt": "find_element_by_link_text",              # "lt": find by link text
    "plt": "find_element_by_partial_link_text",     # "plt": find by partial link text
    "tn": "find_element_by_tag_name",               # "tn": find by tag name
    "cn": "find_element_by_class_name",             # "cn": find by class name
    "cs": "find_element_by_css_selector",           # "cs": find by css selector
}

MULTIPLE_SEARCH_TYPES = {
    "": "find_elements_by_id",
    "id": "find_elements_by_id",
    "x":  "find_elements_by_xpath",
    "n":  "find_elements_by_name",
    "lt": "find_elements_by_link_text",
    "plt": "find_elements_by_partial_link_text",
    "tn": "find_elements_by_tag_name",
    "cn": "find_elements_by_class_name",
    "cs": "find_elements_by_css_selector",
}

SEARCH_BY_TYPES = {
    "": None, # Used for PO
    "id": By.ID,
    "x":  By.XPATH,
    "n":  By.NAME,
    "t": None, # Should never ask for t
    "pn": None, # Should never ask for pn
    "lt": By.LINK_TEXT,
    "plt": By.PARTIAL_LINK_TEXT,
    "tn": By.TAG_NAME,
    "cn": By.CLASS_NAME,
    "cs": By.CSS_SELECTOR,
}


# Error codes
error_codes = {
    "URI Too Long": 414,
    "Bad Request": 400,
    "Not found": 404,
    "Forbidden": 403,
    "Method Not Allowed": 405
}

# Data_types
data_types = {
	"integer": int,
	"string": str,
	"array": list,
	"object": dict
}


# Valid Test Values
valid_body = "body"
valid_project_ids = ["14405","96789","96332","93988"]

# Invalid Test Values
invalid_project_ids = [
    {"value":"555555555", "error code": error_codes["Not found"]},
    {"value":"asd12381asd", "error code": error_codes["Not found"]},
    {"value":"x"*2084, "error code": error_codes["URI Too Long"]},
    {"value":"", "error code": error_codes["Not found"]}
]

# Valid Response formats
response_formats = ['.json', '.xml']
