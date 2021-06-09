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
            url = f"{get_pas_domain()}app/api/v1/app_data/"
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
        self.get(app_id, identifier)

    def create(self, credentials={}):
        try:
            url = f"{get_pas_domain()}app/api/v1/app_user_data/"
            payload = json.dumps({
                "app": self.app_id,
                "identifier": self.identifier,
                "user_creds" : credentials
            })
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            data =response.text
            if response.status_code == 200:
                app_data =  json.loads(data)
                app_data = app_data["data"]
                self.app_user_creds = app_data["user_creds"]
            else:
                return None


        except ObjectDoesNotExist:
            pass

    def get(self):
        try:
            url = f"{get_pas_domain()}app/api/v1/app_user_data/"
            payload = json.dumps({
                "app_id": self.app_id,
                "identifier" : self.identifier
            })
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            data = response.text
            if response.status_code == 200:
                app_data = json.loads(data)
                app_data = app_data["data"]
                self.app_user_creds = app_data["user_creds"]
            else:
                return None
        except ObjectDoesNotExist:
            pass

class AppUserPIM(object):
    def __init__(self, app_id="", app_name="", identifier=""):

        self.app_id= app_id
        self.app_name = app_name
        self.identifier = identifier

    def get(self, app_id, app_name):
        try:
            url = f"{get_pas_domain()}api/v1/app_user_pim_data/"
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
