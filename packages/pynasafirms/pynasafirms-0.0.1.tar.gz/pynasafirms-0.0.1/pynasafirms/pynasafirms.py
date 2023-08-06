# -*- coding: utf-8 -*-
"""API wrapper for NASA's FIRMS API

This module wraps NASA's FIRMS API for usage within python3. NASA's FIRMS API is used to query data
returned by sensors on NASA's satellites which detect active fires around the globe.

Todo:
    * Better exception handling
    * Better tests
"""
import sys
import os
import csv
from datetime import date
import requests
import detection


class NasaFirms:
    """API wrapper class for the NASA FIRMS API

    Attributes:
        self.host           (str): Base hostname for NASA's FIRMS
        self.country_url    (str): API endpoint path for the 'country' endpoint
        self.area_url       (str): API endpoint path for the 'area' endpoint
        self.data_url       (str): API endpoint path for the 'data_availability' endpoint
        self.map_key        (str): Map key provided by NASA FIRMS which is required to query the API

    """
    def __init__(self, map_key: str = None):
        self.host = 'firms.modaps.eosdis.nasa.gov'
        self.country_url = 'https://{0}/api/country/csv/{1}/{2}/{3}/{4}/{5}'
        self.area_url = 'https://{0}/api/area/csv/{1}/{2}/{3}/{4}/{5}'
        self.data_url = 'https://{0}/api/data_availability/csv/{1}/{2}'
        if map_key:
            self.map_key = map_key
        else:
            try:
                self.map_key = os.environ['FIRMS_MAP_KEY']
            except KeyError:
                print('WARNING: No NASA FIRMS Map Key has been passed to the FIRMS obj or set in '
                      'FIRMS_MAP_KEY environment variable')
                sys.exit(1)

    def csv_to_dict(self,
                    csv_data:   bytes,
                    delimiter:  str = ',') -> list:
        """Converts the bytes data returned from the NASA FIRMS API

        The NASA FIRMS API returns bytes encoded comma or semicolon separated values.
        This function decodes the bytes to a utf-8 string, and then leverages the
        'csv' built-in module to convert the comma/semicolon seoarated values into
        a list of dictionaries, and returns it.

        Args:
            csv_data (bytes): bytes encoded comma/semicolon separated values.
            delimiter (str): default delimiter is ','

        Returns:
            list: List of dictionaries containing the decoded and converted api response
        """
        results = []
        decoded_datum = csv_data.decode('utf-8').splitlines()
        parsed_datum = csv.DictReader(decoded_datum, delimiter=delimiter)
        for result in parsed_datum:
            results.append(result)
        return results

    def get_country_modis_nrt(self,
                              country_code: str,
                              days:         int = 1,
                              start_date:   str = date.today().strftime('%Y-%m-%d')) -> list:
        """Queries the '/country' endpoint with the MODIS_NRT sensor

        The country endpoint takes a country code listed on:

        https://firms.modaps.eosdis.nasa.gov/api/countries/?format=html

        It also takes a day range parameter 'days' and a %Y-%m-%d formatted date to query for data
        on said date.
        Info on

        Args:
            country_code (str): Country code
            days (int): Number of days to search from start_date
            start_date (str): Date in %Y-%m-%d format

        Returns:
            list: List of dictionaries containing the decoded and converted api response
        """
        datum = requests.get(self.country_url.format(self.host,
                                                     self.map_key,
                                                     'MODIS_NRT',
                                                     country_code,
                                                     days,
                                                     start_date))
        converted = self.csv_to_dict(datum.content)
        converted = self.response_to_country(converted)
        return converted

    def get_country_modis_sp(self,
                             country_code:  str,
                             days:          int = 1,
                             start_date:    str = date.today().strftime('%Y-%m-%d')) -> list:
        """Queries the '/country' endpoint with the MODIS_SP sensor

        The country endpoint takes a country code listed on:

        https://firms.modaps.eosdis.nasa.gov/api/countries/?format=html

        It also takes a day range parameter 'days' and a %Y-%m-%d formatted date to query for data
        on said date.

        Args:
            country_code (str): Country code
            days (int): Number of days to search from start_date
            start_date (str): Date in %Y-%m-%d format

        Returns:
            list: List of dictionaries containing the decoded and converted api response
        """
        datum = requests.get(self.country_url.format(self.host,
                                                     self.map_key,
                                                     'MODIS_SP',
                                                     country_code,
                                                     days,
                                                     start_date))
        converted = self.csv_to_dict(datum.content)
        converted = self.response_to_country(converted)
        return converted

    def get_country_viirs_noaa20_nrt(self,
                                     country_code:  str,
                                     days:          int = 1,
                                     start_date:    str = date.today().strftime('%Y-%m-%d')) -> list:
        """Queries the '/country' endpoint with the VIIRS_NOAA20_NRT sensor

        The country endpoint takes a country code listed on:

        https://firms.modaps.eosdis.nasa.gov/api/countries/?format=html

        It also takes a day range parameter 'days' and a %Y-%m-%d formatted date to query for data
        on said date.

        Args:
            country_code (str): Country code
            days (int): Number of days to search from start_date
            start_date (str): Date in %Y-%m-%d format

        Returns:
            list: List of dictionaries containing the decoded and converted api response
        """
        datum = requests.get(self.country_url.format(self.host,
                                                     self.map_key,
                                                     'VIIRS_NOAA20_NRT',
                                                     country_code,
                                                     days,
                                                     start_date))
        converted = self.csv_to_dict(datum.content)
        converted = self.response_to_country(converted)
        return converted

    def get_country_viirs_snpp_nrt(self,
                                   country_code:    str,
                                   days:            int = 1,
                                   start_date:      str = date.today().strftime('%Y-%m-%d')) -> list:
        """Queries the '/country' endpoint with the VIIRS_SNPP_NRT sensor

        The country endpoint takes a country code listed on:

        https://firms.modaps.eosdis.nasa.gov/api/countries/?format=html

        It also takes a day range parameter 'days' and a %Y-%m-%d formatted date to query for data
        on said date.

        Args:
            country_code (str): Country code
            days (int): Number of days to search from start_date
            start_date (str): Date in %Y-%m-%d format

        Returns:
            list: List of dictionaries containing the decoded and converted api response
        """
        datum = requests.get(self.country_url.format(self.host,
                                                     self.map_key,
                                                     'VIIRS_SNPP_NRT',
                                                     country_code,
                                                     days,
                                                     start_date))
        converted = self.csv_to_dict(datum.content)
        converted = self.response_to_country(converted)
        return converted

    def get_country_viirs_snpp_sp(self,
                                  country_code: str,
                                  days:         int = 1,
                                  start_date:   str = date.today().strftime('%Y-%m-%d')) -> list:
        """Queries the '/country' endpoint with the VIIRS_SNPP_SP sensor

        The country endpoint takes a country code listed on:

        https://firms.modaps.eosdis.nasa.gov/api/countries/?format=html

        It also takes a day range parameter 'days' and a %Y-%m-%d formatted date to query for data
        on said date.

        Args:
            country_code (str): Country code
            days (int): Number of days to search from start_date
            start_date (str): Date in %Y-%m-%d format

        Returns:
            list: List of dictionaries containing the decoded and converted api response
        """
        datum = requests.get(self.country_url.format(self.host,
                                                     self.map_key,
                                                     'VIIRS_SNPP_SP',
                                                     country_code,
                                                     days,
                                                     start_date))
        converted = self.csv_to_dict(datum.content)
        converted = self.response_to_country(converted)
        return converted

    def get_supported_country_codes(self) -> list:
        """Queries the '/countries' to get all the supported countries.

        https://firms.modaps.eosdis.nasa.gov/api/countries/?format=html

        Args:
            No arguments,

        Returns:
            list: List of dictionaries containing the supported country information
        """

        results = []
        datum = requests.get('https://' + self.host + '/api/countries/')
        parsed_resp = self.csv_to_dict(datum.content, delimiter=';')
        for i in parsed_resp:
            results.append(i)
        return results

    def get_area_modis_nrt(self,
                           area:        str,
                           days:        int = 1,
                           start_date:  str = date.today().strftime('%Y-%m-%d')) -> list:
        """Queries the '/area' endpoint with the MODIS_NRT sensor

        The area endpoint takes compass directions (north, south, east, west) or 'area coordinates'

        Info on the 'area_coordinates' parameter is available at:
        https://firms.modaps.eosdis.nasa.gov/api/area/

        It also takes a day range parameter 'days' and a %Y-%m-%d formatted date to query for data
        on said date.

        Args:
            area (str): Coordinates or compass direction
            days (int): Number of days to search from start_date (minumum 1, max 10)
            start_date (str): Date in %Y-%m-%d format

        Returns:
            list: List of dictionaries containing the decoded and converted api response
        """
        datum = requests.get(self.area_url.format(self.host,
                                                  self.map_key,
                                                  'MODIS_NRT',
                                                  area,
                                                  days,
                                                  start_date))
        converted = self.csv_to_dict(datum.content)
        return converted

    def get_area_modis_sp(self,
                          area:         str,
                          days:         int = 1,
                          start_date:   str = date.today().strftime('%Y-%m-%d')) -> list:
        """Queries the '/area' endpoint with the MODIS_SP sensor

        The area endpoint takes compass directions (north, south, east, west) or 'area coordinates'

        Info on the 'area_coordinates' parameter is available at:
        https://firms.modaps.eosdis.nasa.gov/api/area/

        It also takes a day range parameter 'days' and a %Y-%m-%d formatted date to query for data
        on said date.

        Args:
            area (str): Coordinates or compass direction
            days (int): Number of days to search from start_date (minumum 1, max 10)
            start_date (str): Date in %Y-%m-%d format

        Returns:
            list: List of dictionaries containing the decoded and converted api response
        """
        datum = requests.get(self.area_url.format(self.host,
                                                  self.map_key,
                                                  'VIIRS_SNPP_SP',
                                                  area,
                                                  days,
                                                  start_date))
        converted = self.csv_to_dict(datum.content)
        converted = self.response_to_area(converted)
        return converted

    def get_area_viirs_noaa20_nrt(self,
                                  area:         str,
                                  days:         int = 1,
                                  start_date:   str = date.today().strftime('%Y-%m-%d')) -> list:
        """Queries the '/area' endpoint with the VIIRS_NOAA20_NRT sensor

        The area endpoint takes compass directions (north, south, east, west) or 'area coordinates'

        Info on the 'area_coordinates' parameter is available at:
        https://firms.modaps.eosdis.nasa.gov/api/area/

        It also takes a day range parameter 'days' and a %Y-%m-%d formatted date to query for data
        on said date.

        Args:
            area (str): Coordinates or compass direction
            days (int): Number of days to search from start_date (minumum 1, max 10)
            start_date (str): Date in %Y-%m-%d format

        Returns:
            list: List of dictionaries containing the decoded and converted api response
        """
        datum = requests.get(self.area_url.format(self.host,
                                                  self.map_key,
                                                  'VIIRS_NOAA20_NRT',
                                                  area,
                                                  days,
                                                  start_date))
        converted = self.csv_to_dict(datum.content)
        converted = self.response_to_area(converted)
        return converted

    def get_area_viirs_snpp_nrt(self,
                                area:       str,
                                days:       int = 1,
                                start_date: str = date.today().strftime('%Y-%m-%d')) -> list:
        """Queries the '/area' endpoint with the VIIRS_SNPP_NRT sensor

        The area endpoint takes compass directions (north, south, east, west) or 'area coordinates'

        Info on the 'area_coordinates' parameter is available at:
        https://firms.modaps.eosdis.nasa.gov/api/area/

        It also takes a day range parameter 'days' and a %Y-%m-%d formatted date to query for data
        on said date.

        Args:
            area (str): Coordinates or compass direction
            days (int): Number of days to search from start_date (minumum 1, max 10)
            start_date (str): Date in %Y-%m-%d format

        Returns:
            list: List of dictionaries containing the decoded and converted api response
        """
        datum = requests.get(self.area_url.format(self.host,
                                                  self.map_key,
                                                  'VIIRS_SNPP_NRT',
                                                  area,
                                                  days,
                                                  start_date))
        converted = self.csv_to_dict(datum.content)
        converted = self.response_to_area(converted)
        return converted

    def get_area_viirs_snpp_sp(self,
                               area:        str,
                               days:        int = 1,
                               start_date:  str = date.today().strftime('%Y-%m-%d')) -> list:
        """Queries the '/area' endpoint with the VIIRS_SNPP_SP sensor

        The area endpoint takes compass directions (north, south, east, west) or 'area coordinates'

        Info on the 'area_coordinates' parameter is available at:
        https://firms.modaps.eosdis.nasa.gov/api/area/

        It also takes a day range parameter 'days' and a %Y-%m-%d formatted date to query for data
        on said date.

        Args:
            area (str): Coordinates or compass direction
            days (int): Number of days to search from start_date (minumum 1, max 10)
            start_date (str): Date in %Y-%m-%d format

        Returns:
            list: List of dictionaries containing the decoded and converted api response
        """
        datum = requests.get(self.area_url.format(self.host,
                                                  self.map_key,
                                                  'VIIRS_SNPP_SP',
                                                  area,
                                                  days,
                                                  start_date))
        converted = self.csv_to_dict(datum.content)
        converted = self.response_to_area(converted)
        return converted

    def get_data_availability_all(self) -> list:
        """Queries the '/data_availability' endpoint with all sensors

        Gets the availability of 'date' data for the specified sensor.

        Info on the 'data_availability' endpoint is available at:
        https://firms.modaps.eosdis.nasa.gov/api/data_availability/

        Args:
            No arguments.
        Returns:
            list: List of dictionaries containing the decoded and converted api response
        """
        datum = requests.get(self.data_url.format(self.host, self.map_key, 'ALL'))
        converted = self.csv_to_dict(datum.content)
        converted = self.response_to_area(converted)
        return converted

    def get_data_availability_modis_nrt(self) -> list:
        """Queries the '/data_availability' endpoint with the MODIS_NRT sensor

        Gets the availability of 'date' data for the specified sensor.

        Info on the 'data_availability' endpoint is available at:
        https://firms.modaps.eosdis.nasa.gov/api/data_availability/

        Args:
            No arguments.
        Returns:
            list: List of dictionaries containing the decoded and converted api response
        """
        datum = requests.get(self.data_url.format(self.host, self.map_key, 'MODIS_NRT'))
        converted = self.csv_to_dict(datum.content)
        converted = self.response_to_area(converted)
        return converted

    def get_data_availability_modis_sp(self) -> list:
        """Queries the '/data_availability' endpoint with the MODIS_SP sensor

        Gets the availability of 'date' data for the specified sensor.

        Info on the 'data_availability' endpoint is available at:
        https://firms.modaps.eosdis.nasa.gov/api/data_availability/

        Args:
            No arguments.
        Returns:
            list: List of dictionaries containing the decoded and converted api response
        """
        datum = requests.get(self.data_url.format(self.host, self.map_key, 'MODIS_SP'))
        converted = self.csv_to_dict(datum.content)
        converted = self.response_to_area(converted)
        return converted

    def get_data_availability_viirs_noaa20_nrt(self) -> list:
        """Queries the '/data_availability' endpoint with the VIIRS_NOAA20_NRT sensor

        Gets the availability of 'date' data for the specified sensor.

        Info on the 'data_availability' endpoint is available at:
        https://firms.modaps.eosdis.nasa.gov/api/data_availability/

        Args:
            No arguments.
        Returns:
            list: List of dictionaries containing the decoded and converted api response
        """
        datum = requests.get(self.data_url.format(self.host, self.map_key, 'VIIRS_NOAA20_NRT'))
        converted = self.csv_to_dict(datum.content)
        converted = self.response_to_area(converted)
        return converted

    def get_data_availability_viirs_snpp_sp(self) -> list:
        """Queries the '/data_availability' endpoint with the VIIRS_SNPP_SP sensor

        Gets the availability of 'date' data for the specified sensor.

        Info on the 'data_availability' endpoint is available at:
        https://firms.modaps.eosdis.nasa.gov/api/data_availability/

        Args:
            No arguments.
        Returns:
            list: List of dictionaries containing the decoded and converted api response
        """
        datum = requests.get(self.data_url.format(self.host, self.map_key, 'VIIRS_SNPP_SP'))
        converted = self.csv_to_dict(datum.content)
        converted = self.response_to_area(converted)
        return converted

    def response_to_area(self, response: list) -> list:
        """Converts a response from the 'area' endpoint to an Area class.

        Args:
            response (list): A list of dictionaries containing /area endpoint repsonses
        Returns:
            list: List of Area objects converted from the api response
        """
        converted = []
        if len(response) > 0:
            for resp in response:
                area = detection.detection.Area()
                for key in resp:
                    setattr(area, key, resp[key])
                converted.append(area)
        return converted

    def response_to_country(self, response: list) -> list:
        """Converts a response from the 'area' endpoint to an Area class.

        Args:
            response (list): A list of dictionaries containing /area endpoint repsonses
        Returns:
            list: List of Area objects converted from the api response
        """
        converted = []
        if len(response) > 0:
            for resp in response:
                area = detection.detection.Country()
                for key in resp:
                    setattr(area, key, resp[key])
                converted.append(area)
        return converted
