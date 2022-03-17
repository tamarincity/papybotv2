# flask_app/external_apis/ip_api.py
# test of all  methods of class IpApi
import pytest

from flask_app.constants import (
    URL_IP_API,
)
from flask_app.external_apis.ip_api import IpApi

response_for_malformed_ip = {
    "status": "fail",
    "message": (
        'The IP address is malformed! It should be '
        'as follows: number.number.number.number for instance: 88.23.10.15')}

params = (
    (
        ["Not a string"],
        response_for_malformed_ip),
    (
        '',
        response_for_malformed_ip),
    (
        None,
        response_for_malformed_ip),
    (
        123,
        response_for_malformed_ip),
    (
        'text',
        response_for_malformed_ip),
    (
        '123.14.15.14.12.23',
        response_for_malformed_ip),
    (
        '24.48.0.1',
        {
            "status": "success",
            "country": "Canada",
            "regionName": "Quebec",
            "city": "Montreal",
            "query": "24.48.0.1"})
)

@pytest.mark.parametrize("ip_address, expected_value", [*params])
def test_get_origin_from_ip_address(monkeypatch, ip_address, expected_value):
    print("=> Get origin from IP-address(country, region, city)")

    Sut = IpApi  # class IpApi

    class MockRequestsGet:

        def __init__(self, url) -> None:
            self.url = url

        def json(self):
            if self.url == URL_IP_API + ip_address:
                return expected_value

    mock_requests_get = MockRequestsGet
    monkeypatch.setattr("requests.get", mock_requests_get)

    assert Sut.get_origin_from_ip_address(ip_address) == expected_value
    