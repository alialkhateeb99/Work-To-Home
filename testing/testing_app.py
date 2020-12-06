#tests app.py
from os.path import dirname, join
import sys
sys.path.append(join(dirname(__file__), "../"))


import unittest
import app
import os
import unittest.mock as mock
from mock import patch

KEY_INPUT = "input"
KEY_EXPECTED = "expected"

POSITIVE_TESTING_PARAMETERS = [{KEY_INPUT : "!!!NOT DONE", KEY_EXPECTED: ""},\
{KEY_INPUT : "!!NOT DONE", KEY_EXPECTED: True},\
{KEY_INPUT : {}, KEY_EXPECTED : True },\
{KEY_INPUT : ["9 Corn Drive, CityState, ZZ", 100000, 300000, 30, {}], KEY_EXPECTED : ["9 Corn Drive, CityState, ZZ", 100000, 300000, 30, {}]},\
{KEY_INPUT : ["9 Corn Drive, CityState, ZZ", 100000, 300000, 30], KEY_EXPECTED : ["9 Corn Drive, CityState, ZZ", 100000, 300000, 30]}]
EMAIL = "email"
ADDRESS = "address"
PRICE_RANGE_LOW = "price_range_low"
PRICE_RANGE_HIGH = "price_range_high"
CITY = "city"
STATE = "state"
DISTANCE = "max_commute"
MIN_PRICE = "min_price"
MAX_PRICE = "max_price"
PURCHASE_TYPE = "purchase_type"
# class MockSendToDatabase(unittest.TestCase):
#     def setUp(self):
#         self.success_test_params = {
#             KEY_INPUT: {
#                 EMAIL: "kevinng250",
#                 ADDRESS: "141 Summit Street, Newark, NJ",
#                 PRICE_RANGE_LOW: "100",
#                 PRICE_RANGE_HIGH: "2000" 
#             },
#             KEY_EXPECTED: ""
#         }
class MockParsingSearchParameters(unittest.TestCase):
    def setUp(self):
        self.success_test_params = {
            KEY_INPUT: {
                ADDRESS:"141 Summit Street",
                CITY:"Newark",
                STATE:"NJ",
                DISTANCE:"40",
                MIN_PRICE:100,
                MAX_PRICE:2000,
                PURCHASE_TYPE: "sale"
            },
            KEY_EXPECTED: None
        }
        
    def mock_get_homes(self, city, state, min_price, max_price, absolute_address):
        return -1
    def mock_get_homes_exists(self, city, state, min_price, max_price, absolute_address):
        return 1
    def mock_send_To_database(self, email, address, price_range_low, price_range_high, distance, city, state, purchase_type):
        return None
        
    @patch('flask_socketio.SocketIO.emit')
    def test_parse_search_parameters(self, mock_socket):
        test_case = self.success_test_params
        with mock.patch("app.send_to_database", self.mock_send_To_database):
            with mock.patch("apifunctions.get_homes", self.mock_get_homes):
                result = app.parsing_search_parameters(test_case[KEY_INPUT])
                mock_socket.assert_called_with('sending listing', [])
    
    @patch('flask_socketio.SocketIO.emit')
    def test_parse_search_parameters_exists(self, mock_socket):
        test_case = self.success_test_params
        with mock.patch("app.send_to_database", self.mock_send_To_database):
            with mock.patch("apifunctions.get_homes", self.mock_get_homes_exists):
                result = app.parsing_search_parameters(test_case[KEY_INPUT])
                mock_socket.assert_called_with('sending listing', 1)
                
class MockDisplayTable(unittest.TestCase):
    def setUp(self):
        self.success_test_params = {
            KEY_INPUT: "asdf@njit.edu",
            KEY_EXPECTED:None
        }
    def mock_db_query(self):
        return ["hello","hello"]
    def mock_db_query_no_rows(self):
        return None
    
    @patch('flask_socketio.SocketIO.emit')
    def test_displayTable(self, mock_socket):
        test_case = self.success_test_params
        with mock.patch("app.DB.session") as mock_query:
            mock_query.query.return_value.filter_return_value.all.return_value = self.mock_db_query()
            result = app.display_table()
            self.assertTrue(mock_socket.called)
            mock_socket.assert_called_with("received database info", [])
    
    @patch('flask_socketio.SocketIO.emit')
    def test_displayTable_norows(self, mock_socket):
        test_case = self.success_test_params
        with mock.patch("app.DB.session", new_callable=mock.PropertyMock) as mock_query:
            mock_query.query.return_value.filter_return_value.all.return_value = self.mock_db_query_no_rows()
            result = app.display_table()
            # self.assertTrue(mock_socket.called)
            mock_socket.assert_called_with("received database info", [])    
        
if __name__ == "__main__":
    unittest.main()