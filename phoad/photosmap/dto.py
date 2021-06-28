class Location:
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude


class LocationValidator:
    @staticmethod
    def validate(latitude: float, longitude: float) -> Location:
        if not latitude or not longitude:
            raise InvalidLocationArguments("Latitude and longitude must not be null")
        try:
            latitude = float(latitude)
            longitude = float(longitude)
            return Location(latitude, longitude)
        except Exception:
            raise InvalidLocationArguments("Latitude and longitude must be float numbers")


class LocationThreshold:
    def __init__(self, threshold: int):
        self.threshold = threshold


class LocationThresholdValidator:
    @staticmethod
    def validate(threshold: int) -> LocationThreshold:
        if not threshold:
            raise InvalidLocationArguments("Threshold must not be null")
        try:
            threshold = int(threshold)
            return LocationThreshold(threshold)
        except Exception:
            raise InvalidLocationArguments("Threshold must be integer number")


class LocationDiff:
    def __init__(self, min_latitude, max_latitude, min_longitude, max_longitude):
        self.min_latitude = min_latitude
        self.max_latitude = max_latitude
        self.min_longitude = min_longitude
        self.max_longitude = max_longitude

    @staticmethod
    def from_location(location: Location, loc_threshold: LocationThreshold):
        return LocationDiff(location.latitude - loc_threshold.threshold, location.latitude + loc_threshold.threshold,
                            location.longitude - loc_threshold.threshold, location.latitude + loc_threshold.threshold)


class InvalidLocationArguments(Exception):
    pass
