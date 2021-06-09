import json
import requests

from common.utils.utility import get_pim_app_domain, get_pas_domain, get_pim_domain
from common.pim_catalog.pim.exceptions import TokenExpiredException


class PIM(object):
    def __init__(self, api_key):
        self.base_url = get_pim_domain()
        self.api_key = api_key
        self.headers = {
            "Authorization": api_key,
            'content-type': "application/json"
        }

    def all(self):
        pass

    def import_to_pim(self):
        pass

    def register(self):
        pass

    def uninstall(self):
        """
            Method to uninstall app from PIM.
        :return:
        """
        self.send_request("{}/pim/v1/unInstall".format(self.base_url), "DELETE", {}, headers=self.headers)

    def send_request(self, url, method, data=None, headers=None):
        if not data:
            data = dict()
        if not headers:
            headers = dict()
        response = requests.request(
            method=method, url=url, data=json.dumps(data), headers=headers
        )
        if response.status_code in [200, 201, 202]:
            return response
        elif response.status_code == 401:
            raise TokenExpiredException("Token expired")
        else:
            raise ValueError("Error while fetching : {}".format(response.text))
