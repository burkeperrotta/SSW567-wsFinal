import unittest
from unittest.mock import patch
from pt3MRTD import MRTDSystem  # Replace 'your_module_name' with the actual module name

class TestMRTDSystem(unittest.TestCase):

    def test_scan_mrz(self):
        line = "P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<;W620126G54CIV5910106F9707302AJ010215I<<<<<<6"
        result = MRTDSystem.scan_mrz(line)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertEqual(result, ("P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<", "W620126G54CIV5910106F9707302AJ010215I<<<<<<6"))
        
    def test_scan_mrz_2(self):
        line = "abc"
        result = MRTDSystem.scan_mrz(line)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertEqual(result, (line, ""))

    def test_decode_mrz_line(self):
        # You can create test cases for the decode_mrz_line method
        # Mocking the check_digit method to isolate the test
        with patch.object(MRTDSystem, 'check_digit', return_value='1'):
            line1 = "P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<"
            line2 = "W620126G54CIV5910106F9707302AJ010215I<<<<<<6"
            decoded_info = MRTDSystem.decode_mrz_line(line1, line2, 0)
            self.assertIsInstance(decoded_info, dict)
            # Add more assertions based on the expected output

    def test_encode_mrz_line(self):
        # You can create test cases for the encode_mrz_line method
        line1_data = {
        "issuing_country": "CIV",
        "last_name": "LYNN",
        "given_name": "NEVEAH BRAM"
      }
        line2_data = {
        "passport_number": "W620126G5",
        "country_code": "CIV",
        "birth_date": "591010",
        "sex": "F",
        "expiration_date": "970730",
        "personal_number": "AJ010215I"
      }
        encoded1, encoded2 = MRTDSystem.encode_mrz_line(line1_data, line2_data)
        self.assertEqual(encoded1+";"+encoded2, "P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<;W620126G54CIV5910106F9707302AJ010215I<<<<<<6")
        # Add more assertions based on the expected output

    def test_decode_mrz(self):
        # You can create test cases for the decode_mrz method
        # Mocking the scan_mrz and decode_mrz_line methods to isolate the test
        with patch.object(MRTDSystem, 'scan_mrz', return_value=('line1', 'line2')):
            with patch.object(MRTDSystem, 'decode_mrz_line', return_value={}):
                decoded_records = MRTDSystem.decode_mrz(2)
                self.assertIsInstance(decoded_records, list)
                self.assertEqual(len(decoded_records), 2)
                # Add more assertions based on the expected output

    def test_encode_mrz(self):
        # You can create test cases for the encode_mrz method
        # Mocking the encode_mrz_line method to isolate the test
        with patch.object(MRTDSystem, 'encode_mrz_line', return_value=('encoded1', 'encoded2')):
            encoded_records = MRTDSystem.encode_mrz(2)
            self.assertIsInstance(encoded_records, list)
            self.assertEqual(len(encoded_records), 2)
            # Add more assertions based on the expected output

    def test_check_digit(self):        
        check_digit_result = MRTDSystem.check_digit("ABC123")
        self.assertIsInstance(check_digit_result, str)    

    # Add more test cases as needed

if __name__ == '__main__':
    unittest.main()