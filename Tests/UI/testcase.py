'this file contains test cases'

import unittest
import os

from libs import builtins, utils, setup_variables
#from libs.setup_variables import init_driver
from selenium import webdriver
import json
from libs import driver

class TestUI(unittest.TestCase):

    def setUp(self):
        self.driver = builtins.DRIVER
        self.driver.get(builtins.BASE_URL)
        utils.wait_for_page_to_load()

    def test_search_one_result(self):
        utils.i_fill_in_the_object_with_text("Search Input", "DYNACULT")
        utils.i_click_the_object("Search button")
        utils.wait_for_page_to_load()
        utils.current_page_is("Search Results page")
        utils.wait_for_element_to_be_present("Counter div")
        try:
            self.assertEqual("1",utils.find_element("Counter div").text.strip())
        except:
            raise ValueError("Actual result: \"{}\" | Expected: \"{}\"".format(utils.find_element("Counter div").text.strip(), "1"))

    def test_search_ten_results(self):
        utils.i_clear_the_object("Search Input")
        utils.i_fill_in_the_object_with_text("Search Input", "Cytometer")
        utils.i_click_the_object("Search button")
        utils.wait_for_page_to_load()
        utils.current_page_is("Search Results page")
        utils.wait_for_element_to_be_present("Counter div")
        try:
            self.assertGreater(int(utils.find_element("Counter div").text.strip()), 10)
        except:
            raise ValueError(
                "Actual result: \"{}\" | Expected: \"{}\"".format(utils.find_element("Counter div").text.strip(), "more than 10"))


if __name__ == '__main__':
    unittest.main()