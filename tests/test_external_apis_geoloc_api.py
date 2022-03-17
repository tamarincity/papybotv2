# flask_app/external_apis/geoloc_api.py
# test of all  methods of class GeolocApi

from flask_app.constants import (
    CENTER_OF_FRANCE,
)
from flask_app.external_apis.geoloc_api import GeolocApi
from env import (
    api_key,
    app_id,
)

url_api_key = f"&apiKey={api_key}"
url_app_id = f"&app_id={app_id}"

def test_check_if_city_exists(monkeypatch):
    print("=> Check if the geoloc API knows the city")

    city = "paris"
    Sut = GeolocApi  # class GeolocApi
    expected_value = {
        "Response": {
            "View": [
                {"Result": [
                    {"Location": {
                        "Address":{
                            "City": "Paris"}}}]}]}}
    class MockRequestsGet:
        def __init__(self, url):
            pass

        def json(cls):
            return expected_value

    monkeypatch.setattr("requests.get", MockRequestsGet)
    assert Sut.check_if_city_exists("") == None
    assert Sut.check_if_city_exists(city) == expected_value


def test_request_to_geoloc_api(monkeypatch):
    print(
        "=> get address, latitude and longitude"
        "of a location from the geoloc API")
    Sut = GeolocApi  # class GeolocApi
    url_from_france = f"at={CENTER_OF_FRANCE}&"
    url_question1 = "q=openclassrooms&"
    url_question2 = ""
    url_city_out_of_question1 = "qq=city=paris&"
    url_city_out_of_question2 = ""
    url_api_key = f"apiKey={api_key}"

    full_url1 = (
            url_from_france
            + url_question1
            + url_city_out_of_question1
            + url_api_key
        )
    full_url2 = (
            url_from_france
            + url_question1
            + url_city_out_of_question2
            + url_api_key
        )
    full_url3 = (
            url_from_france
            + url_question2
            + url_city_out_of_question1
            + url_api_key
        )
    full_url4 = (
            url_from_france
            + url_question2
            + url_city_out_of_question2
            + url_api_key
        )
    full_url5 = (
            url_from_france
            + url_question2
            + url_city_out_of_question2
        )
    value_for_good_request = {
        "results": [
            {
                "title": "Openclassrooms",
                "vicinity": "10 Cité Paradis<br/>75010 Paris",
                "position": [
                    48.87511,
                    2.34897
                ],
                "category": "education-facility"}]}

    value_for_location_missing_in_request = {
        "status": 400,
        "message": "Required query parameter 'q' is not present",
        "incidentId": "3bdc3f30-dfe0-4faa-9c3f-30dfe01faa69"}

    value_for_no_credential_found_in_request = {
        "error": "Unauthorized",
        "error_description": "No credentials found"}

    class MockRequestsGet:
        def __init__(self, url):
            self.url = url

        def json(self):
            key_for_city = "&qq="
            key_for_location_to_find = "&q="
            

            # If location, city and api_key are in the url
            if full_url1 in self.url:
                expected_value = value_for_good_request

            # If location and api_key are in the url but not the city
            elif full_url2 in self.url and key_for_city not in self.url:
                expected_value = value_for_good_request

            # If location is missing in the url
            elif key_for_location_to_find not in self.url:
                expected_value = value_for_location_missing_in_request

            # If api_key is missing in the url
            if url_api_key not in self.url:
                expected_value = value_for_no_credential_found_in_request
            return expected_value

    monkeypatch.setattr("requests.get", MockRequestsGet)
    assert Sut.request_to_geoloc_api(full_url1) == value_for_good_request
    assert Sut.request_to_geoloc_api(full_url2) == value_for_good_request
    assert Sut.request_to_geoloc_api(full_url3) == value_for_location_missing_in_request
    assert Sut.request_to_geoloc_api(full_url4) == value_for_location_missing_in_request
    assert Sut.request_to_geoloc_api(full_url5) == value_for_no_credential_found_in_request


def test_get_interesting_points_around(monkeypatch):
    print("=> Get interesting points around a latitude and a longitude")
    Sut = GeolocApi  # class GeolocApi
    latitude = 43.604425
    longitude = 1.443802
    response_of_request = {
        "results": {
            "items": [
                {
                    "position": [
                        43.604425,
                        1.443802
                    ],
                    "distance": 0,
                    "title": "Cour Henri IV",
                    "averageRating": 0.0,
                    "category": {
                        "id": "landmark-attraction",
                        "title": "Landmark/Attraction",
                        "href": "https://places.sit.ls.hereapi.com/places/v1/categories/places/landmark-attraction?app_id=app_id&app_code=app_code",
                        "type": "urn:nlp-types:category",
                        "system": "places"
                    },
                    "icon": "https://download.vcdn.cit.data.here.com/p/d/places2_stg/icons/categories/38.icon",
                    "vicinity": "Parking Capitole<br/>31000 Toulouse",
                    "having": [],
                    "type": "urn:nlp-types:place",
                    "href": "https://places.sit.ls.hereapi.com/places/v1/places/2508lxx5-2ec5572ed59d084799522fd169861a3e;context=Zmxvdy1pZD04YzUxZWM4YS1hNmNmLTUyYTctYTI1YS00ZWQ4OGRkMTkwNTdfMTY0Mjc4NDU2MDQ4NV83NTI4XzMxMzEmcmFuaz0w?app_id=app_id&app_code=app_code",
                    "id": "2508lxx5-2ec5572ed59d084799522fd169861a3e"
    }]}}

    expected_value = [
        {
            "position": [
                43.604425,
                1.443802
            ],
            "distance": 0,
            "title": "Cour Henri IV",
            "averageRating": 0.0,
            "category": {
                "id": "landmark-attraction",
                "title": "Landmark/Attraction",
                "href": "https://places.sit.ls.hereapi.com/places/v1/categories/places/landmark-attraction?app_id=app_id&app_code=app_code",
                "type": "urn:nlp-types:category",
                "system": "places"
            },
            "icon": "https://download.vcdn.cit.data.here.com/p/d/places2_stg/icons/categories/38.icon",
            "vicinity": "Parking Capitole<br/>31000 Toulouse",
            "having": [],
            "type": "urn:nlp-types:place",
            "href": "https://places.sit.ls.hereapi.com/places/v1/places/2508lxx5-2ec5572ed59d084799522fd169861a3e;context=Zmxvdy1pZD04YzUxZWM4YS1hNmNmLTUyYTctYTI1YS00ZWQ4OGRkMTkwNTdfMTY0Mjc4NDU2MDQ4NV83NTI4XzMxMzEmcmFuaz0w?app_id=app_id&app_code=app_code",
            "id": "2508lxx5-2ec5572ed59d084799522fd169861a3e"
}]
    class MockRequestsGet:
        def __init__(self, url):
            self.url = url

        def json(self):
            return response_of_request

    monkeypatch.setattr("requests.get", MockRequestsGet)
    assert Sut.get_interesting_points_around(latitude, longitude) == expected_value
