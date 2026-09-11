# ============================================
# WORD MILES - CITY GEOCODING
#
# Turns a city name a player types into map
# coordinates using OpenStreetMap (no API key
# needed). Results are cached so the same city
# is never looked up twice, and any failure
# (typo, network hiccup, service down) is
# handled gracefully -- the game should never
# crash because a lookup failed.
# ============================================

import functools
import math

from geopy.geocoders import Nominatim


_geolocator = Nominatim(user_agent="word-miles-friendship-game", timeout=5)


@functools.lru_cache(maxsize=256)
def geocode_city(city_name):
    """
    Looks up a city name and returns {"lat", "lon"},
    or None if it can't be found.
    """

    city_name = city_name.strip()

    if not city_name:
        return None

    try:
        location = _geolocator.geocode(city_name)
    except Exception:
        return None

    if location is None:
        return None

    return {
        "lat": location.latitude,
        "lon": location.longitude
    }


def haversine_km(lat1, lon1, lat2, lon2):
    """
    Great-circle distance between two coordinates, in km.
    """

    earth_radius_km = 6371

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    )

    return 2 * earth_radius_km * math.asin(math.sqrt(a))
