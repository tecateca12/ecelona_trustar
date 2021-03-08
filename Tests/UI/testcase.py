"""
Title: Test Project search UI Tech Port
Description:
    - Testing search keywords:
        - DYNACULT: displays exactly one result
        - Cytometer: displays more than ten results
"""

import unittest
import os
from libs import builtins, utils, setup_variables


class TestUI(unittest.TestCase):

    def setUp(self):
        self.driver = builtins.DRIVER

    def test_search_one_result_counterDiv(self):
        '''
            Make sure that there just 1 result row
        '''
        self.driver.get(builtins.BASE_URL)
        utils.wait_for_page_to_load()
        utils.i_fill_in_the_object_with_text("Search Input", "DYNACULT")
        utils.i_click_the_object("Search button")
        utils.wait_for_page_to_load()
        utils.current_page_is("Search Results page")
        utils.wait_for_element_to_be_present("Counter div")
        try:
            self.assertEqual("1",utils.find_element("Counter div").text.strip())
        except:
            raise ValueError("Actual result: \"{}\" | Expected: \"{}\"".format(utils.find_element("Counter div").text.strip(), "1"))

    def test_search_one_result_pagination(self):
        '''
            Make sure that pagination displays valid text
        '''
        utils.wait_for_element_to_be_present("Paginator text")
        # validate page 1 of 1 is displayed
        try:
            self.assertTrue(''.join([x for x in utils.find_element("Paginator text").find_element_by_tag_name('input').get_attribute('value') if x.isdigit()]) == '1')
        except:
            raise ValueError("Actual result: \"{}\" | Expected: \"{}\"".format(''.join([x for x in utils.find_element("Paginator text").find_element_by_tag_name('input').get_attribute('value') if x.isdigit()]), "1"))
        try:
            self.assertTrue(''.join([x for x in utils.find_element("Paginator text").text if x.isdigit()]) == '1')
        except:
            raise ValueError("Actual result: \"{}\" | Expected: \"{}\"".format(''.join([x for x in utils.find_element("Paginator text").text if x.isdigit()]), "1"))

    def test_search_one_result_rows(self):
        '''
            Make sure that there just 1 result row
        '''
        utils.wait_for_element_to_be_present("Result row")
        try:
            self.assertTrue(len(utils.find_elements("Result row")) == 1)
        except:
            raise ValueError("Actual result: \"{}\" | Expected: \"{}\"".format(len(utils.find_elements("Result row")), "1"))

    def test_search_ten_results_counterDiv(self):
        '''
            Make sure that there are more than 10 results
        '''
        utils.i_clear_the_object("Search Input")
        utils.i_fill_in_the_object_with_text("Search Input", "Cytometer")
        utils.i_click_the_object("Search button")
        utils.wait_for_page_to_load()
        utils.current_page_is("Search Results page")
        utils.wait_for_element_to_be_present("Counter div")
        try:
            # NOTE: This test is not connected to the API, so we are just validating that the results number is
            # greater than 10, Ideally the results qty must be compared against the endpoint
            self.assertGreater(int(utils.find_element("Counter div").text.strip()), 10)
        except:
            raise ValueError(
                "Actual result: \"{}\" | Expected: \"{}\"".format(utils.find_element("Counter div").text.strip(), "more than 10"))

    def test_search_ten_results_pagination(self):
        '''
            Make sure that pagination displays valid text
        '''
        utils.wait_for_element_to_be_present("Paginator text")
        # validate page 1 of 1 is displayed
        # NOTE: since I don't have documentation about the search component not sure how many results per page are supposed to be displayed
        # ideally the number must not be hardcoded as "1 of 1" as in this tests example.
        try:
            self.assertTrue(''.join([x for x in utils.find_element("Paginator text").find_element_by_tag_name(
            'input').get_attribute('value') if x.isdigit()]) == '1')
        except:
            raise ValueError("Actual result: \"{}\" | Expected: \"{}\"".format(''.join([x for x in utils.find_element("Paginator text").find_element_by_tag_name(
            'input').get_attribute('value') if x.isdigit()]), "1"))

        try:
            self.assertTrue(''.join([x for x in utils.find_element("Paginator text").text if x.isdigit()]) == '1')
        except:
            raise ValueError("Actual result: \"{}\" | Expected: \"{}\"".format(''.join([x for x in utils.find_element("Paginator text").text if x.isdigit()]), "1"))

    def test_search_ten_results_rows(self):
        '''
            Make sure that there more than 10 results rows
        '''
        utils.wait_for_element_to_be_present("Result row")
        # NOTE: This test is not connected to the API, so we are just validating that the results number is
        # greater than 10, Ideally the results qty must be compared against the endpoint
        try:
            self.assertTrue(len(utils.find_elements("Result row")) > 10)
        except:
            raise ValueError("Actual result: \"{}\" | Expected: \"{}\"".format(len(utils.find_elements("Result row")), "more than 10"))

if __name__ == '__main__':
    unittest.main()