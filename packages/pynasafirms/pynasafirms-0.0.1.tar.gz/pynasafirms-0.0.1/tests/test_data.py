import unittest
import pynasafirms


class TestArea(unittest.TestCase):

    def setUp(self) -> None:
        self.nf = pynasafirms.NasaFirms()

    def test_get_data_availability_all(self):
        self.assertEqual(self.nf.get_data_availability_all()[0].data_id, 'MODIS_NRT')

    def test_get_data_availability_modis_nrt(self):
        self.assertEqual(self.nf.get_data_availability_modis_nrt()[0].data_id, 'MODIS_NRT')

    def test_get_data_availability_modis_sp(self):
        self.assertEqual(self.nf.get_data_availability_modis_sp()[0].data_id, 'MODIS_SP')

    def test_get_data_availability_viirs_noaa20_nrt(self):
        self.assertEqual(self.nf.get_data_availability_viirs_noaa20_nrt()[0].data_id,
                         'VIIRS_NOAA20_NRT')

    def test_get_data_availability_viirs_snpp_sp(self):
        self.assertEqual(self.nf.get_data_availability_viirs_snpp_sp()[0].data_id,
                         'VIIRS_SNPP_SP')


if __name__ == '__main__':
    unittest.main()
