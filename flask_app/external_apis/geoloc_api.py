import requests

from ..constants import (
    URL_GEOLOCATION_API,
    URL_GET_CITY_GEOLOC_API,
    URL_GET_INTERESTING_POINTS_AROUND,
)

from env import (
    api_key,
    app_id,
)

url_api_key = f"&apiKey={api_key}"
url_app_id = f"&app_id={app_id}"


class GeolocApi:
    @classmethod
    def check_if_city_exists(cls, city):
        if city:
            return requests.get(URL_GET_CITY_GEOLOC_API + city + url_api_key).json()
        else:
            return None

    @classmethod
    def request_to_geoloc_api(cls, full_url):
        response = requests.get(URL_GEOLOCATION_API + full_url)
        if response:
            return response.json()
        return None

    @classmethod
    def get_interesting_points_around(cls, latitude, longitude):
        try:
            response = requests.get(
                URL_GET_INTERESTING_POINTS_AROUND
                + f"{latitude},{longitude}"
                + url_api_key
                + url_app_id
            ).json()["results"]["items"]
            return response
        except Exception as e:
            return str(e)
