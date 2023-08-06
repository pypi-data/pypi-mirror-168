# pyNASAFIRMS
[![License: GNU AGPL v3](https://img.shields.io/badge/license-GNU%20AGPL%20v3-blue)](https://github.com/PlantDaddy/pyNASAFIRMS/blob/main/LICENSE)[![Contributor Covenant: v2.1 adopted](https://img.shields.io/badge/Contributor%20Covenant-v2.1%20adopted-pink)](https://img.shields.io/badge/Contributor%20Covenant-v2.1%20adopted-pink)[![Python versions: >= 3.7](https://img.shields.io/pypi/pyversions/pyNASAFIRMS)](https://img.shields.io/pypi/pyversions/pyNASAFIRMS)

Слава Україні:ukraine:/Slava Ukraini :ukraine:!

Fuck :russia:

pyNASAFIRMS is a wrapper for NASA's FIRMS API. Covers all the endpoints that FIRMS supports as of 08/22/2022.

## Requirements
This requires Python >= 3.7. In reality it likely works on more but this is what it was developed with. 

Packages required:

- requests

## Quick Start
First off, you NEED to get a 'map key' from NASA to query the API: [Get it here.](https://firms.modaps.eosdis.nasa.gov/api/area/)

At the bottom of the page, theres a 'Map Key' section. Click the 'Get MAP_KEY' button. 

Once you have a map key, you can set an environment variable ```FIRMS_MAP_KEY``` to equal the map key provided by NASA. Otherwise, you can pass a map key to the ```NasaFirms``` object via the ```NasaFirms.map_key``` attribute. 

```python
import pynasafirms
client = pynasafirms.NasaFirms(map_key='xxxxxxxxxx')
resp = client.get_country_modis_nrt('UKR')
print(resp[0].longitude)
....
29.24976
```
The above code queries the FIRMS 'country' endpoint with the country code 'UKR' (Ukraine) and the ```MODIS_NRT``` sensor. It also has a default parameter for the 'start_date' to be queried. If a date isn't specified, the current local date is used in YYYY-MM-DD and passed to the endpoint. The 'days' defaults 1 unless specified. The FIRMS endpoints only allow for up to 10 days, but this isn't enforced in the wrapper(yet). After the query returns, a list of 'Country' objects are returned.

Info on the NASA FIRMS api [here](https://firms.modaps.eosdis.nasa.gov/api/).