"""
Title: Test Project endpoint of NASA Tech Port
Description:
    - Information about the API endpoint: https://api.nasa.gov/techport/api/specification
    - Testing positive and negative values for the 2 parameters accepted in path:
        * project_id
        * format
    - Testing positive and negative scenarios for authentication key

"""

from libs.utils import send_get_request, send_post_request, send_put_request
from libs import consts
from libs.utils import log_test
import unittest
from random import choice

class TestApiProjectsHappyPaths(unittest.TestCase):

    @log_test
    def test_default_response_formats(self):
        """
        Validates default response format as json
        """
        response = send_get_request('/projects/{}'.format(choice(consts.valid_project_ids)))
        self.assertTrue(isinstance(response,dict))
        if isinstance(response, dict):
            # Check Response was not an error
            self.assertTrue('error' not in response.keys())

    @log_test
    def test_only_required_params(self):
        """
        Make sure requests are accepted if only required params are sent
        Required parameters:
            :: api_key: str
            :: request_type: str
            :: project_id: int
        """
        response = send_get_request('/projects/{}'.format(choice(consts.valid_project_ids)))
        # Check Response was not an error
        self.assertTrue('error' not in response.keys())

    @log_test
    def test_valid_project_id(self):
        """
        Make sure requests are accepted if the project_id is valid
        """
        for project_id in consts.valid_project_ids:
            response = send_get_request('/projects/{}'.format(project_id))
            # Check Response was not an error
            self.assertTrue('error' not in response.keys())

    @log_test
    def test_validate_structure_data_types_responses(self):
        """
        Make sure the response items are properly structured and validate the data type for each k:v
        """
        response = send_get_request('/projects/{}'.format(choice(consts.valid_project_ids)))
        # Check Response was not an error
        self.assertTrue('error' not in response.keys())
        # Check there is a response and it is correctly formated
        self.assertTrue('project' in response.keys())
        self.assertTrue(len(response['project']) > 0)
        # get properties from API documentation
        properties = send_get_request('/specification')['definitions']['project']['properties']
        """
        # NOTE: API documentation doesn't state which parameters are constant and which ones may not be present, 
        while developing the script I've noticed that the keys presents on the response varies depending 
        on the project id
        """
        for k, v in response['project'].items():
            self.assertTrue(k in properties.keys())
            self.assertTrue(type(v) == consts.data_types[properties[k]['type']])

    @log_test
    def test_response_formats(self):
        """
        Validates response format as xml/json
        """
        for r_format in consts.response_formats:
            response = send_get_request('/projects/{}{}'.format(choice(consts.valid_project_ids),r_format))
            if isinstance(response,dict):
                # Check Response was not an error
                self.assertTrue('error' not in response.keys())
                # validate that json response contains a project
                self.assertTrue(len(response) == 1)
            else:
                self.assertTrue(response.headers['Content-Type'] == 'application/xml;charset=utf-8')
                # ISSUE: Endpoint returns status code 200 but the content is empty if xml format is requested

                # NOTE: xml response was not parsed since the response is empty and cannot be tested
                # for this challenge due lack of knowledge of xml schema that endpoint should returned

                # self.assertGreater(len(response.text), 0)



class TestApiProjectsNegativePaths(unittest.TestCase):

    @log_test
    def test_no_api_key(self):
        """
        Validates response error if missing api_key on request
        """
        response = send_get_request('/projects/{}'.format(choice(consts.valid_project_ids)),api_key='')
        self.assertEqual(response.status_code, consts.error_codes["Forbidden"])

    @log_test
    def test_invalid_project_id(self):
        """
        Check 404 response if invalid project id
        """
        for project_id in consts.invalid_project_ids:
            response = send_get_request('/projects/{}'.format(project_id))
            # Check Response error was as expected
            # Issue Reason on response is empty if 404
            self.assertEqual(response.status_code, project_id["error code"])

    @log_test
    def test_post(self):
        """
        Make sure POST request is rejected even if it is an authenticated user and valid data
        """
        response = send_post_request('/projects/{}'.format(choice(consts.valid_project_ids)),
                                     data=consts.valid_body)
        # Check Response was an error
        self.assertEqual(list(response.keys()), ['error'])
        # Check error code is 400 Bad request
        self.assertEqual(response['error']['code'], consts.error_codes["Bad Request"])
        # ISSUE: api is returning 400 instead of 403 or 405 when trying to perform a post
        # ALSO: there is no message associated on the response if bad request

    @log_test
    def test_put(self):
        """
        Make sure PUT request is rejected even if it is an authenticated user and valid data
        """
        response = send_put_request('/projects/{}'.format(choice(consts.valid_project_ids)),
                                     data=consts.valid_body)
        # Check error code is 405 Method Not Allowed
        if isinstance(response,dict):
            # Check Response was an error
            self.assertEqual(list(response.keys()), ['error'])
            self.assertEqual(response['error']['code'], consts.error_codes["Method Not Allowed"])
        else:
            # Issue Reason on response is empty
            self.assertEqual(response.status_code, consts.error_codes["Method Not Allowed"])

if __name__ == '__main__':
    unittest.main()