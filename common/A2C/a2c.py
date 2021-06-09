from django.core.exceptions import ObjectDoesNotExist
import logging
from django.conf import settings
import requests
import json
from common.utils.utility import get_pim_app_domain, get_pas_domain
logger = logging.getLogger(__name__)

class App(object):
    def __init__(self, app_id="", app_name=""):
        self.app_id= app_id
        self.app_name = app_name
        self.get(app_id, app_name)

    def create(self, app_id, name, credentials={}):
        try:
            url = f"{get_pas_domain()}api/v1/app/"

            payload = json.dumps({
                "app_id": app_id,
                "name": name,
                "credentials" : credentials
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

    def get(self, app_id, app_name):
            try:
                url = f"{get_pas_domain()}app/api/v1/app_data/"

                payload = json.dumps({
                    "app_id": app_id,
                })
                headers = {
                    'Content-Type': 'application/json'
                }

                response = requests.request("GET", url, headers=headers, data=payload)

                data =response.text

                if response.status_code == 200:

                    app_data =  json.loads(data)
                    app_data = app_data["data"]
                    self.app_creds = app_data["credentials"]
                    self.app_name = app_data["app_data"]["name"]
                    self.app_id = app_data["app_data"]["label"]
                    return app_data
                else:
                    return None

            except ObjectDoesNotExist:
                pass


class AppUser(object):
    def __init__(self, app_id, identifier):
        self.app_id= app_id
        self.identifier= identifier
        self.app_user_creds= self.get(app_id, identifier)

    def create(self, app_id, identifier, credentials={}):
        try:

            url = f"{get_pas_domain()}api/v1/app_user/"


            payload = json.dumps({
                "app": app_id,
                "identifier": identifier,
                "user_creds" : credentials
            })
            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status == 200:
                return {
                    "app": app_id,
                    "identifier": identifier,
                    "user_creds" : credentials
                }
            else:
                return None


        except ObjectDoesNotExist:
            pass

    def get(self, app_id, identifier):
        try:
            url = f"{get_pas_domain()}api/v1/app_user/"

            payload = json.dumps({
                "app_id": app_id,
                "identifier" :identifier
            })
            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.request("GET", url, headers=headers, data=payload)

            data =response.text
            if response.status == 200:
                return data
            else:
                return None

        except ObjectDoesNotExist:
            pass

