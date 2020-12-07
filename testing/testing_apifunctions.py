from os.path import dirname, join
import sys
sys.path.append(join(dirname(__file__), "../"))

import unittest
import os
import unittest.mock as mock
from mock import patch, call
import apifunctions
from apifunctions import HOME_CITY, HOME_STREET, HOME_POSTAL_CODE,\
                            HOME_STATE_CODE, HOME_STATE, HOME_COUNTY, \
                            HOME_PRICE, HOME_BATHS, HOME_BEDS, HOME_IMAGE, \
                            HOME_LAT, HOME_LON, IFRAME_URL, COMMUTE_TIME, \
                            HOME_WALKSCORE, WALKSCORE_DESCRIPTION, \
                            WALKSCORE_LOGO, WALKSCORE_MORE_INFO_LINK,\
                            HOME_WALKSCORE_LINK
import requests
import io
import google_maps_api

KEY_INPUT = "input"
KEY_EXPECTED = "expected"

PROPERTY_ID = "property_id"
MIN_PRICE = "min_price"
MAX_PRICE = "max_price"
ABSOLUTE_ADDRESS = "absolute_address"

CITY = "city"
STATE_CODE = "state_code"

class MockedResponse:
    def __init__(self, json_data):
        self.json_data = json_data
    def json(self):
        return self.json_data

class MockNearbyHomes(unittest.TestCase):
    def setUp(self):
        self.success_test_params = {
            KEY_INPUT: {
                PROPERTY_ID: "111111",
                MIN_PRICE: 0,
                MAX_PRICE: 1000000,
                ABSOLUTE_ADDRESS: "141 Summit St, Newark, NJ"
            },
            KEY_EXPECTED:[{
                HOME_CITY: "Newark",
                HOME_STREET:"141 Summit Street",
                HOME_POSTAL_CODE:"07103",
                HOME_STATE_CODE:34,
                HOME_STATE: "NJ",
                HOME_COUNTY: "Essex",
                HOME_PRICE:2000,
                HOME_BATHS:2,
                HOME_BEDS:2,
                HOME_IMAGE:"filler_url",
                HOME_LON:"filler_longitude",
                HOME_LAT:"filler_latitude",
                IFRAME_URL:"some url",
                COMMUTE_TIME:"something",
                HOME_WALKSCORE:"hello",
                WALKSCORE_DESCRIPTION:"sup",
                WALKSCORE_LOGO:"something",
                WALKSCORE_MORE_INFO_LINK:"something",
                HOME_WALKSCORE_LINK:"something else"
            }]
        }
    def mock_success_requests(self, method, url, headers, params):
        d = {
            "data":{
                "home":{
                    "related_homes":{
                        "results":[
                            {
                                "list_price": 2000,
                                "location":{
                                    "address":{
                                        "line" : "141 Summit Street",
                                        "city" : "Newark"
                                    }
                                },
                                "description":{
                                    "baths":2,
                                    "beds":2
                                },
                                "primary_photo":{
                                    "href":"filler_url"
                                }
                            }
                        ]
                    }
                }
            }
        }
        r = MockedResponse(d)
        return r

    def mock_success_geocode(self, address):
        return [
            {
                "address_components":["","","",
                    {"long_name":"Essex"},
                    {"short_name":34,"long_name":"NJ"},"",
                    {"long_name":"07103"}
                ],
                "geometry":{
                    "location":{
                        "lng": "filler_longitude",
                        "lat": "filler_latitude"
                    }
                }
            }
        ]
    def mock_walkscore_info(self, home_street, home_city, home_state_code, home_lon, home_lat):
        return {
            "walkscore" : "hello",
            "description": "sup",
            "logo" : "something",
            "more_info_link":"something",
            "walkscore_link":"something else"
        }
    
    def mock_generate_iframe_url(self, origin, destination):
        return "some url"
        
    def mock_get_place_id(self, address):
        return "some place"
        
    
    def mock_directions(self, address, address2, mode, departure_time):
        return [{
                "legs":[
                    {
                    "duration":{
                        "text" : "something"
                        }
                    }
                ]   
        }]

    def test_nearbyHomes_success(self):
        test_case = self.success_test_params
        with mock.patch("requests.request", self.mock_success_requests):
            with mock.patch("googlemaps.Client.geocode", self.mock_success_geocode):
                with mock.patch("google_maps_api.get_place_id", self.mock_get_place_id):
                    with mock.patch("google_maps_api.generate_iframe_url", self.mock_generate_iframe_url):
                        with mock.patch("googlemaps.Client.directions", self.mock_directions):
                            with mock.patch("walkscore_api.get_walkscore_info", self.mock_walkscore_info):
                                inp = test_case[KEY_INPUT]
                                results = apifunctions.nearby_homes(inp[PROPERTY_ID], inp[MIN_PRICE], inp[MAX_PRICE], inp[ABSOLUTE_ADDRESS])
                                for result in results:
                                    # print(result)
                                    # print(test_case[KEY_EXPECTED][0])
                                    self.assertDictEqual(result, test_case[KEY_EXPECTED][0])
    
    # def mock_stdout(self):
    #     return "getHomes API : Http Error: ", requests.exceptions.HTTPError
    
    def mock_HTTPError_requests(self, method, url, headers, params):
        return requests.exceptions.HTTPError
    
    def test_nearbyHomes_HTTPErr(self):
        test_case = self.success_test_params
        with mock.patch("requests.request") as barMock:
            barMock.side_effect = requests.exceptions.HTTPError
            inp = test_case[KEY_INPUT]
            result = apifunctions.nearby_homes(inp[PROPERTY_ID], inp[MIN_PRICE], inp[MAX_PRICE], inp[ABSOLUTE_ADDRESS])
            
    def test_nearbyHomes_ConnectionErr(self):
        test_case = self.success_test_params
        with mock.patch("requests.request") as barMock:
            barMock.side_effect = requests.exceptions.ConnectionError
            inp = test_case[KEY_INPUT]
            result = apifunctions.nearby_homes(inp[PROPERTY_ID], inp[MIN_PRICE], inp[MAX_PRICE], inp[ABSOLUTE_ADDRESS])
    
    def test_nearbyHomes_Timeout(self):
        test_case = self.success_test_params
        with mock.patch("requests.request") as barMock:
            barMock.side_effect = requests.exceptions.Timeout
            inp = test_case[KEY_INPUT]
            result = apifunctions.nearby_homes(inp[PROPERTY_ID], inp[MIN_PRICE], inp[MAX_PRICE], inp[ABSOLUTE_ADDRESS])
            
    def test_nearbyHomes_RequestException(self):
        test_case = self.success_test_params
        with mock.patch("requests.request") as barMock:
            barMock.side_effect = requests.exceptions.RequestException
            inp = test_case[KEY_INPUT]
            result = apifunctions.nearby_homes(inp[PROPERTY_ID], inp[MIN_PRICE], inp[MAX_PRICE], inp[ABSOLUTE_ADDRESS])
            
    def test_nearbyHomes_IndexError(self):
        test_case = self.success_test_params
        with mock.patch("requests.request") as barMock:
            barMock.side_effect = IndexError
            inp = test_case[KEY_INPUT]
            result = apifunctions.nearby_homes(inp[PROPERTY_ID], inp[MIN_PRICE], inp[MAX_PRICE], inp[ABSOLUTE_ADDRESS])
        
class MockGetHomes(unittest.TestCase):
    def setUp(self):
        self.success_test_params = {
            KEY_INPUT: {
                CITY: "Newark",
                STATE_CODE: "34",
                MIN_PRICE: 0,
                MAX_PRICE: 1000000,
                ABSOLUTE_ADDRESS: "141 Summit St, Newark, NJ"
            },
            KEY_EXPECTED:[{
                HOME_CITY: "Newark",
                HOME_STREET:"141 Summit Street",
                HOME_POSTAL_CODE:"07103",
                HOME_STATE_CODE:"34",
                HOME_STATE: "NJ",
                HOME_PRICE:2000,
                HOME_BATHS:2,
                HOME_BEDS:2,
                HOME_IMAGE:"filler_url",
                HOME_LON:"filler_longitude",
                HOME_LAT:"filler_latitude",
                IFRAME_URL:"some url",
                COMMUTE_TIME:"something",
                HOME_WALKSCORE:"hello",
                WALKSCORE_DESCRIPTION:"sup",
                WALKSCORE_LOGO:"something",
                WALKSCORE_MORE_INFO_LINK:"something",
                HOME_WALKSCORE_LINK:"something else"
            },
            {
                HOME_CITY: "Newark",
                HOME_STREET:"141 Summit Street",
                HOME_POSTAL_CODE:"07103",
                HOME_STATE_CODE:"34",
                HOME_STATE: "NJ",
                HOME_COUNTY: "Essex",
                HOME_PRICE:2000,
                HOME_BATHS:2,
                HOME_BEDS:2,
                HOME_IMAGE:"filler_url",
                HOME_LON:"filler_longitude",
                HOME_LAT:"filler_latitude",
                IFRAME_URL:"some url",
                COMMUTE_TIME:"something",
                HOME_WALKSCORE:"hello",
                WALKSCORE_DESCRIPTION:"sup",
                WALKSCORE_LOGO:"something",
                WALKSCORE_MORE_INFO_LINK:"something",
                HOME_WALKSCORE_LINK:"something else"
            }]
        }
        self.success_test_params_no_properties = {
            KEY_INPUT: {
                CITY: "Newark",
                STATE_CODE: "34",
                MIN_PRICE: 0,
                MAX_PRICE: 1000000,
                ABSOLUTE_ADDRESS: "141 Summit Street, Newark, NJ"
            },
            KEY_EXPECTED:-1
        }
        self.success_test_params_no_thumbnail = {
            KEY_INPUT: {
                CITY: "Newark",
                STATE_CODE: 34,
                MIN_PRICE: 0,
                MAX_PRICE: 1000000,
                ABSOLUTE_ADDRESS: "141 Summit Street, Newark, NJ"
            },
            KEY_EXPECTED:[{
                HOME_CITY: "Newark",
                HOME_STREET:"141 Summit Street",
                HOME_POSTAL_CODE:"07103",
                HOME_STATE_CODE:"34",
                HOME_STATE: "NJ",
                HOME_PRICE:2000,
                HOME_BATHS:2,
                HOME_BEDS:2,
                HOME_IMAGE:"DEFAULT_IMAGE",
                HOME_LON:"filler_longitude",
                HOME_LAT:"filler_latitude",
                IFRAME_URL:"some url",
                COMMUTE_TIME:"something",
                HOME_WALKSCORE:"hello",
                WALKSCORE_DESCRIPTION:"sup",
                WALKSCORE_LOGO:"something",
                WALKSCORE_MORE_INFO_LINK:"something",
                HOME_WALKSCORE_LINK:"something else"
            },
            {
                HOME_CITY: "Newark",
                HOME_STREET:"141 Summit Street",
                HOME_POSTAL_CODE:"07103",
                HOME_STATE_CODE:"34",
                HOME_STATE: "NJ",
                HOME_COUNTY: "Essex",
                HOME_PRICE:2000,
                HOME_BATHS:2,
                HOME_BEDS:2,
                HOME_IMAGE:"filler_url",
                HOME_LON:"filler_longitude",
                HOME_LAT:"filler_latitude",
                IFRAME_URL:"some url",
                COMMUTE_TIME:"something",
                HOME_WALKSCORE:"hello",
                WALKSCORE_DESCRIPTION:"sup",
                WALKSCORE_LOGO:"something",
                WALKSCORE_MORE_INFO_LINK:"something",
                HOME_WALKSCORE_LINK:"something else"
            }]
        }
    def mock_success_requests_properties(self, method, url, headers, params):
        d = {
            "meta":{
                "returned_rows":2
            },
            "properties":[{
                    "thumbnail":"filler_url",
                    "price":2000,
                    "address":{
                        "city":"Newark",
                        "line":"141 Summit Street",
                        "postal_code": "07103",
                        "state_code": "34",
                        "state": "NJ",
                        "lon":"filler_longitude",
                        "lat":"filler_latitude"
                    },
                    "baths":2,
                    "beds":2,
                    "property_id":12345
                },
                {
                    "thumbnail":"filler_url",
                    "price":10000000,
                    "address":{
                        "city":"Newark",
                        "line":"141 Summit Street",
                        "postal_code": "07103",
                        "state_code": 34,
                        "state": "NJ",
                        "lon":"filler_longitude",
                        "lat":"filler_latitude"
                    },
                    "baths":2,
                    "beds":2,
                    "property_id":12345
                }
            ]
        }
        r = MockedResponse(d)
        return r
        
    def mock_nearbyHomes(self, PROPERTY_ID, MIN_PRICE, MAX_PRICE, ABSOLUTE_ADDRESS):
        return [{
             HOME_CITY: "Newark",
                HOME_STREET:"141 Summit Street",
                HOME_POSTAL_CODE:"07103",
                HOME_STATE_CODE:"34",
                HOME_STATE: "NJ",
                HOME_COUNTY: "Essex",
                HOME_PRICE:2000,
                HOME_BATHS:2,
                HOME_BEDS:2,
                HOME_IMAGE:"filler_url",
                HOME_LON:"filler_longitude",
                HOME_LAT:"filler_latitude",
                IFRAME_URL:"some url",
                COMMUTE_TIME:"something",
                HOME_WALKSCORE:"hello",
                WALKSCORE_DESCRIPTION:"sup",
                WALKSCORE_LOGO:"something",
                WALKSCORE_MORE_INFO_LINK:"something",
                HOME_WALKSCORE_LINK:"something else"
            }
        ]
    def mock_walkscore_info(self, home_street, home_city, home_state_code, home_lon, home_lat):
        return {
            "walkscore" : "hello",
            "description": "sup",
            "logo" : "something",
            "more_info_link":"something",
            "walkscore_link":"something else"
        }
    
    def mock_generate_iframe_url(self, origin, destination):
        return "some url"
        
    def mock_get_place_id(self, address):
        return "some place"
        
    def mock_geocode(self, address):
        return "geocode"
    
    def mock_directions(self, address, address2, mode, departure_time):
        return [{
                "legs":[
                    {
                    "duration":{
                        "text" : "something"
                        }
                    }
                ]   
        }]
    def test_getHomes_success(self):
        test_case = self.success_test_params
        with mock.patch("requests.request", self.mock_success_requests_properties):
            with mock.patch("apifunctions.nearby_homes", self.mock_nearbyHomes):
                with mock.patch("walkscore_api.get_walkscore_info", self.mock_walkscore_info):
                    with mock.patch("google_maps_api.generate_iframe_url", self.mock_generate_iframe_url):
                        with mock.patch("google_maps_api.get_place_id", self.mock_get_place_id):
                            with mock.patch("googlemaps.Client.directions", self.mock_directions):
                                inp = test_case[KEY_INPUT]
                                results = apifunctions.get_homes(inp[CITY], inp[STATE_CODE], inp[MIN_PRICE], inp[MAX_PRICE], inp[ABSOLUTE_ADDRESS])
                                print(inp[MIN_PRICE])
                                print(inp[MAX_PRICE])
                                for i in range(len(results)):
                                    self.assertDictEqual(results[i], test_case[KEY_EXPECTED][i])
    
    def mock_success_requests_properties_none(self, method, url, headers, params):
        d = {
            "meta":{
                "returned_rows":0
            }
        }
        r = MockedResponse(d)
        return r
    
    def test_getHomes_success_no_properties(self):
        test_case = self.success_test_params_no_properties
        with mock.patch("requests.request", self.mock_success_requests_properties_none):
            with mock.patch("apifunctions.nearby_homes", self.mock_nearbyHomes):
                with mock.patch("walkscore_api.get_walkscore_info", self.mock_walkscore_info):
                    with mock.patch("google_maps_api.generate_iframe_url", self.mock_generate_iframe_url):
                        with mock.patch("google_maps_api.get_place_id", self.mock_get_place_id):
                            with mock.patch("googlemaps.Client.directions", self.mock_directions):
                                inp = test_case[KEY_INPUT]
                                results = apifunctions.get_homes(inp[CITY], inp[STATE_CODE], inp[MIN_PRICE], inp[MAX_PRICE], inp[ABSOLUTE_ADDRESS])
                                self.assertEquals(results, test_case[KEY_EXPECTED])
                
    def mock_success_requests_properties_no_thumbnail(self, method, url, headers, params):
        d = {
            "meta":{
                "returned_rows":1
            },
            "properties":[{
                    "price":2000,
                    "address":{
                        "city":"Newark",
                        "line":"141 Summit Street",
                        "postal_code": "07103",
                        "state_code": "34",
                        "state": "NJ",
                        "lon":"filler_longitude",
                        "lat":"filler_latitude"
                    },
                    "baths":2,
                    "beds":2,
                    "property_id":12345
                }
            ]
        }
        r = MockedResponse(d)
        return r
        
    def test_getHomes_success_no_thumbnail(self):
        test_case = self.success_test_params_no_thumbnail
        with mock.patch("requests.request", self.mock_success_requests_properties_no_thumbnail):
            with mock.patch("apifunctions.nearby_homes", self.mock_nearbyHomes):
                with mock.patch("walkscore_api.get_walkscore_info", self.mock_walkscore_info):
                    with mock.patch("google_maps_api.generate_iframe_url", self.mock_generate_iframe_url):
                        with mock.patch("google_maps_api.get_place_id", self.mock_get_place_id):
                            with mock.patch("googlemaps.Client.directions", self.mock_directions):
                                inp = test_case[KEY_INPUT]
                                results = apifunctions.get_homes(inp[CITY], inp[STATE_CODE], inp[MIN_PRICE], inp[MAX_PRICE], inp[ABSOLUTE_ADDRESS])
                                for i in range(len(results)):
                                    self.assertDictEqual(results[i], test_case[KEY_EXPECTED][i])
    
    # @patch('requests.request')
    # @patch('apifunctions.nearbyHomes')
    # @patch('builtins.print')
    def test_getHomes_HTTPErr(self):
        test_case = self.success_test_params
        with mock.patch("requests.request") as barMock:
            barMock.side_effect = requests.exceptions.HTTPError
            inp = test_case[KEY_INPUT]
            result = apifunctions.get_homes(inp[CITY], inp[STATE_CODE], inp[MIN_PRICE], inp[MAX_PRICE], inp[ABSOLUTE_ADDRESS])
        
    def test_getHomes_ConnectionErr(self):
        test_case = self.success_test_params
        with mock.patch("requests.request") as barMock:
            barMock.side_effect = requests.exceptions.ConnectionError
            inp = test_case[KEY_INPUT]
            result = apifunctions.get_homes(inp[CITY], inp[STATE_CODE], inp[MIN_PRICE], inp[MAX_PRICE], inp[ABSOLUTE_ADDRESS])
    
    def test_getHomes_Timeout(self):
        test_case = self.success_test_params
        with mock.patch("requests.request") as barMock:
            barMock.side_effect = requests.exceptions.Timeout
            inp = test_case[KEY_INPUT]
            result = apifunctions.get_homes(inp[CITY], inp[STATE_CODE], inp[MIN_PRICE], inp[MAX_PRICE], inp[ABSOLUTE_ADDRESS])
            
    def test_getHomes_RequestException(self):
        test_case = self.success_test_params
        with mock.patch("requests.request") as barMock:
            barMock.side_effect = requests.exceptions.RequestException
            inp = test_case[KEY_INPUT]
            result = apifunctions.get_homes(inp[CITY], inp[STATE_CODE], inp[MIN_PRICE], inp[MAX_PRICE], inp[ABSOLUTE_ADDRESS])
            
    def test_getHomes_IndexError(self):
        test_case = self.success_test_params
        with mock.patch("requests.request") as barMock:
            barMock.side_effect = IndexError
            inp = test_case[KEY_INPUT]
            result = apifunctions.get_homes(inp[CITY], inp[STATE_CODE], inp[MIN_PRICE], inp[MAX_PRICE], inp[ABSOLUTE_ADDRESS])
            
class MockGetPlaceId(unittest.TestCase):
    def setUp(self):
        self.success_test_params = {
            KEY_INPUT: "141 Summit St, Newark, NJ",
            KEY_EXPECTED: "some_id"
        }
    
    def mock_find_place(self, address, input_type):
        return {
                "candidates":[{
                    "place_id": "some_id"
                    }
                ]
            }
        
    def test_get_place_id(self):
        test_case = self.success_test_params
        with mock.patch("googlemaps.Client.find_place", self.mock_find_place):
            result = google_maps_api.get_place_id(test_case[KEY_INPUT])
            self.assertEqual(result, test_case[KEY_EXPECTED])
    
if __name__ == "__main__":
    unittest.main()