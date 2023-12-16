import unittest
from unittest.mock import patch
from MRTD.py import MRTDSystem 


class TestMRTDSystem(unittest.TestCase):

    def test_scan_mrz(self):
        with patch('builtins.input', return_value=''), patch('builtins.print'):  # Mock input and print
            result = MRTDSystem.scan_mrz()
            self.assertIsInstance(result, tuple)
            self.assertEqual(len(result), 2)

    def test_decode_mrz(self):
        line1 = "P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<"
        line2 = "L898902C<3UTO6908061F9406236ZE184226B<<<<<10"
        result = MRTDSystem.decode_mrz(line1, line2)
        self.assertIsInstance(result, dict)
        self.assertEqual(result['Name'], 'UTOERIKSSON<<ANNA<MARIA')

    def test_encode_mrz(self):
        info_fields = {
            'Type': 'P', 'IssuingCountry': 'UTO', 'Name': 'ERIKSSON<<ANNA<MARIA',
            'PassportNumber': 'L898902C<', 'CountryCode': '3UT', 'BirthDate': '069080', 'Gender': '6',
            'ExpirationDate': '1F9406', 'PersonalNumber': '236ZE184226B<<<<<10',
            'CheckDigit1': '3', 'CheckDigit2': '6', 'CheckDigit3': '6', 'CheckDigit4': '0'
        }
        result = MRTDSystem.encode_mrz(info_fields)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

    def test_database_interaction(self):
        #database interaction
        with patch('builtins.print'):
            MRTDSystem.database_interaction({})

    def test_report_mismatch(self):
        mrz_fields = {
            'CheckDigit1': '3', 'CheckDigit2': '6', 'CheckDigit3': '6', 'CheckDigit4': '0'
        }
        with patch('builtins.print') as mock_print:
            MRTDSystem.report_mismatch(mrz_fields)
            mock_print.assert_called_with("Mismatch in CheckDigit1: 3 is incorrect.")

if __name__ == '__main__':
    unittest.main()
