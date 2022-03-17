import re
from typing import List

import requests

from ..constants import (
    URL_IP_API,
)


class IpApi:

    @classmethod
    def get_origin_from_ip_address(cls, ip_address):

        # In the "if" below when testing locally with the browser
        if ip_address in ["127.0.0.1", "192.168.1.41", "localhost"]:
            return {
                "status": "success",
                "city": "La ville où il y a ton ordi",
                "region": "Là où tu te trouves",
                "country": "Le pays où tu es en ce moment"}

        # The variable "response" is the response to be returned by this method
        response = {
            "status": "fail",
            "message": (
                'The IP address is malformed! It should be '
                'as follows: number.number.number.number for instance: 88.23.10.15')}

        if not (ip_address and isinstance(ip_address, str)):
            return response

        regex_pattern = r"\d+(\.\d+){3}"  # Format of IP-address
        found = re.search(regex_pattern, ip_address)     
        if found and found.group(0) == ip_address:
            response = requests.get(URL_IP_API + ip_address)
            return response.json()

        return response
