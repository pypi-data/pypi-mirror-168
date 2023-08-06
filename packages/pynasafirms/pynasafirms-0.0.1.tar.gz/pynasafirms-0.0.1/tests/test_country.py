import unittest
import pynasafirms


class TestCountry(unittest.TestCase):

    def setUp(self) -> None:
        self.nf = pynasafirms.NasaFirms()

    def test_country_modis_nrt(self):
        self.assertEqual(self.nf.get_country_modis_nrt('UKR', start_date='2022-04-04')[0].country_id,
                         'UKR')

    def test_country_modis_sp(self):
        self.assertEqual(self.nf.get_country_modis_sp('UKR', start_date='2022-04-04'), [])

    def test_country_viirs_noaa20_nrt(self):
        self.assertEqual(self.nf.get_country_viirs_noaa20_nrt('UKR', start_date='2022-04-04')[0].country_id, 'UKR')

    def test_country_viirs_snpp_nrt(self):
        self.assertEqual(self.nf.get_country_viirs_snpp_nrt('UKR', start_date='2022-04-04')[0].country_id,
                         'UKR')

    def test_country_viirs_snpp_sp(self):
        self.assertEqual(self.nf.get_country_viirs_snpp_sp('UKR', start_date='2022-04-04'), [])

    def test_get_supported_countries(self):
        self.assertEqual(self.nf.get_supported_country_codes()[0]['id'], '1')


if __name__ == '__main__':
    unittest.main()
