import unittest
import pynasafirms


class TestArea(unittest.TestCase):

    def setUp(self) -> None:
        self.nf = pynasafirms.NasaFirms()

    def test_get_area_modis_nrt(self):
        self.assertEqual(self.nf.get_area_modis_nrt('22.132839803,44.381048895,40.159543091,52.36894928',
                                                    start_date='2022-04-04')[0]['acq_date'],
                         '2022-04-04')

    def test_get_area_modis_sp(self):
        self.assertEqual(self.nf.get_area_modis_sp('22.132839803,44.381048895,40.159543091,52.36894928',
                                                   start_date='2022-04-04'), [])

    def test_get_area_viirs_noaa20_nrt(self):
        self.assertEqual(self.nf.get_area_viirs_noaa20_nrt('22.132839803,44.381048895,40.159543091,'
                                                           '52.36894928',
                                                           start_date='2022-04-04')[0].acq_date,
                         '2022-04-04')

    def test_get_area_viirs_snpp_nrt(self):
        self.assertEqual(self.nf.get_area_viirs_snpp_nrt('22.132839803,44.381048895,40.159543091,'
                                                         '52.36894928',
                                                         start_date='2022-04-04')[0].acq_date,
                         '2022-04-04')

    def test_get_area_viirs_snpp_sp(self):
        self.assertEqual(self.nf.get_area_viirs_snpp_sp('22.132839803,44.381048895,40.159543091,'
                                                        '52.36894928',
                                                        start_date='2022-04-04'), [])


if __name__ == '__main__':
    unittest.main()