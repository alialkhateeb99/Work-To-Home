#tests models.py
from os.path import dirname, join
import sys
sys.path.append(join(dirname(__file__), "../"))

import unittest
import models
import os
import unittest.mock as mock


KEY_INPUT = "input"
KEY_EXPECTED = "expected"

POSITIVE_TESTING_PARAMETERS = [
    {KEY_INPUT : {"email" : "hello@njit.edu", "address" : "9 Corn Drive, CityState, ZZ", "price_range_low" : 100000, "price_range_high" : 300000, "distance": 10}, 
    KEY_EXPECTED : True },\
    {
    KEY_INPUT : ["hello@njit.edu", "9 Corn Drive, CityState, ZZ", 100000, 300000, 30, "CityState", "ZZ", "sale"], 
    KEY_EXPECTED : ["hello@njit.edu", "9 Corn Drive, CityState, ZZ", 100000, 300000, 30, "CityState", "ZZ", "sale"]},\
    {KEY_INPUT : ["9 Corn Drive, CityState, ZZ", 100000, 300000, 30], KEY_EXPECTED : ["9 Corn Drive, CityState, ZZ", 100000, 300000, 30]}]

class TestingModels(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [\
            {KEY_INPUT : ["hello@njit.edu", "9 Corn Drive, CityState, ZZ", 100000, 300000, 30, "CityState", "ZZ", "sale"],\
            KEY_EXPECTED : ["hello@njit.edu", "9 Corn Drive, CityState, ZZ", 100000, 300000, 30, "CityState", "ZZ", "sale"]}]
            
    def check_class__table_defintion(self, testing_parameter):
        expected = testing_parameter[KEY_EXPECTED]
        input_data = testing_parameter[KEY_INPUT]
        input_address = input_data[1]
        input_email = input_data[0];  input_dist = input_data[4];
        input_low = input_data[2];  input_high = input_data[3]; 
        input_city = input_data[5]; input_state = input_data[6];
        input_purchase_type = input_data[7]
        print(expected)
        reference_not_perm = models.TableDefintion(input_email, input_address, input_low, input_high, input_dist, input_city, input_state, input_purchase_type)
        if(reference_not_perm.email == expected[0] and reference_not_perm.address == expected[1]):#use is instead of == ?????
            if(reference_not_perm.price_low == expected[2] and reference_not_perm.price_high == expected[3] and reference_not_perm.distance == expected[4]):
                if(reference_not_perm.city == expected[5] and reference_not_perm.state == expected[6] and reference_not_perm.purchase_type == expected[7]):
                    return True
        return False
            
    def test_success_test_params(self):
        test_eval = self.check_class__table_defintion(POSITIVE_TESTING_PARAMETERS[1])
        #test_eval_2 = check_class__table_defintion(POSITIVE_TESTING_PARAMETERS[1])
        #test_eval_3 = mock_addition(POSITIVE_TESTING_PARAMETERS[0])
        
if __name__ == '__main__':
    unittest.main()
    