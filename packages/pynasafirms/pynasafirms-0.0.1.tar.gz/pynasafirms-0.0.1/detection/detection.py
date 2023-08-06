class Area:
    def __init__(self,
                 latitude:      str = None,
                 longitude:     str = None,
                 bright_ti4:    str = None,
                 scan:          str = None,
                 track:         str = None,
                 acq_date:      str = None,
                 acq_time:      str = None,
                 satellite:     str = None,
                 instrument:    str = None,
                 confidence:    str = None,
                 version:       str = None,
                 bright_ti5:    str = None,
                 frp:           str = None,
                 daynight:      str = None,
                 brightness:    str = None,
                 bright_t31:    str = None):
        self.latitude = latitude
        self.longitude = longitude
        self.bright_ti4 = bright_ti4
        self.scan = scan
        self.track = track
        self.acq_date = acq_date
        self.acq_time = acq_time
        self.satellite = satellite
        self.instrument = instrument
        self.confidence = confidence
        self.version = version
        self.bright_ti5 = bright_ti5
        self.frp = frp
        self.daynight = daynight
        self.brightness = brightness
        self.bright_t31 = bright_t31

    def __str__(self):
        return f"Area(latitude={self.latitude}, " \
               f"longitude={self.longitude}, " \
               f"bright_ti4={self.bright_ti4}, " \
               f"scan={self.scan}, " \
               f"track={self.track}, " \
               f"acq_date={self.acq_date}, " \
               f"acq_time={self.acq_time}, " \
               f"satellite={self.satellite}, " \
               f"instrument={self.instrument}, " \
               f"confidence={self.version}, " \
               f"bright_ti5={self.bright_ti5}, " \
               f"frp={self.frp}, " \
               f"daynight={self.daynight}, " \
               f"brightness={self.brightness}, " \
               f"bright_t31={self.bright_t31}"

    def __repr__(self):
        return f"Area(latitude={self.latitude}, " \
               f"longitude={self.longitude}, " \
               f"bright_ti4={self.bright_ti4}, " \
               f"scan={self.scan}, " \
               f"track={self.track}, " \
               f"acq_date={self.acq_date}, " \
               f"acq_time={self.acq_time}, " \
               f"satellite={self.satellite}, " \
               f"instrument={self.instrument}, " \
               f"confidence={self.version}, " \
               f"bright_ti5={self.bright_ti5}, " \
               f"frp={self.frp}, " \
               f"daynight={self.daynight}, " \
               f"brightness={self.brightness}, " \
               f"bright_t31={self.bright_t31}"


class Country:
    def __init__(self,
                 country_id:    str = None,
                 latitude:      str = None,
                 longitude:     str = None,
                 bright_ti4:    str = None,
                 scan:          str = None,
                 track:         str = None,
                 acq_date:      str = None,
                 acq_time:      str = None,
                 satellite:     str = None,
                 instrument:    str = None,
                 confidence:    str = None,
                 version:       str = None,
                 bright_ti5:    str = None,
                 frp:           str = None,
                 daynight:      str = None,
                 brightness:    str = None,
                 bright_t31:    str = None):
        self.country_id = country_id
        self.latitude = latitude
        self.longitude = longitude
        self.bright_ti4 = bright_ti4
        self.scan = scan
        self.track = track
        self.acq_date = acq_date
        self.acq_time = acq_time
        self.satellite = satellite
        self.instrument = instrument
        self.confidence = confidence
        self.version = version
        self.bright_ti5 = bright_ti5
        self.frp = frp
        self.daynight = daynight
        self.brightness = brightness
        self.bright_t31 = bright_t31

    def __str__(self):
        return f"Country(country_id={self.country_id}, " \
               f"latitude={self.latitude}, " \
               f"longitude={self.longitude}, " \
               f"bright_ti4={self.bright_ti4}, " \
               f"scan={self.scan}, " \
               f"track={self.track}, " \
               f"acq_date={self.acq_date}, " \
               f"acq_time={self.acq_time}, " \
               f"satellite={self.satellite}, " \
               f"instrument={self.instrument}, " \
               f"confidence={self.confidence}, " \
               f"version={self.version}, " \
               f"bright_ti5={self.bright_ti5}, " \
               f"frp={self.frp}, " \
               f"daynight={self.daynight}, " \
               f"brightness={self.brightness}, " \
               f"bright_t31={self.bright_t31})"

    def __repr__(self):
        return f"Country(country_id={self.country_id}, " \
               f"latitude={self.latitude}, " \
               f"longitude={self.longitude}, " \
               f"bright_ti4={self.bright_ti4}, " \
               f"scan={self.scan}, " \
               f"track={self.track}, " \
               f"acq_date={self.acq_date}, " \
               f"acq_time={self.acq_time}, " \
               f"satellite={self.satellite}, " \
               f"instrument={self.instrument}, " \
               f"confidence={self.confidence}, " \
               f"version={self.version}, " \
               f"bright_ti5={self.bright_ti5}, " \
               f"frp={self.frp}, " \
               f"daynight={self.daynight}, " \
               f"brightness={self.brightness}, " \
               f"bright_t31={self.bright_t31})"
