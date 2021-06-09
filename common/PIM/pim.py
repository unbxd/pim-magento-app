from django.core.exceptions import ObjectDoesNotExist
import logging
from django.conf import settings
import requests
import json
from common.utils.utility import get_pim_app_domain, get_pas_domain
logger = logging.getLogger(__name__)

class Installer(object):
    def __init__(self, app_id="", app_name="", identifier=""):

        self.app_id= app_id
        self.app_name = app_name
        self.identifier = identifier

    def install(self,pim_data):
        try:
            url = f"{get_pas_domain()}pim/sso_install/"

            payload = json.dumps({
                "org_key" : pim_data['orgKey'],
                "site_name" : pim_data['siteName'],
                "app_id": self.app_id,
                "identifier": self.identifier,
                "cookie" : pim_data["cookie"]
            })
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            data =response.text
            if response.status == 200:
                return data
            else:
                return None

        except ObjectDoesNotExist:
            pass




