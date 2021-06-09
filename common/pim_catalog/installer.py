import json
import requests

from app_mgr.models import PimProp
from django.conf import settings


def get_pim_domain():
    return getattr(settings, "PIM_BASE_URL")


class Installer(object):

    def install(self, org_key, site_name, auth_token, app_id, user, cookie=None, source=None):

        payload = dict()
        payload["appCustomId"] = app_id
        payload["siteName"] = site_name
        headers = {
            'content-type': "application/json"
        }
        if cookie:
            cookies_obj = {"_un_sso_uid": cookie}
            url = get_pim_domain() + "/api/v3/" + org_key + "/register"
            response = requests.request("POST", url, data=json.dumps(payload), headers=headers, cookies=cookies_obj)
        else:
            url = get_pim_domain() + "/v2/register"
            payload["orgKey"] = org_key
            headers["Authorization"] = auth_token
            response = requests.request("POST", url, data=json.dumps(payload), headers=headers)



        if response.status_code != 200:
            raise ValueError(
                "Pim Authorization failed: status: {} body : {}".format(str(response.status_code), response.text)
            )

        if "data" not in response.json() or "apiKey" not in response.json()["data"]:
            raise ValueError("Pim Authorization failed due to data expectation")

        api_key = response.json()["data"]["apiKey"]
        PimProp.objects.update_or_create(user=user, api_key=api_key, org_key=org_key, site_name=site_name)
